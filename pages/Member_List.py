import streamlit as st
import requests
from congress import Congress
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page

from const import STATE_DICT

# Config webapp
st.set_page_config(
    page_title="BillBriefs",
    # page_icon=":chart_with_upwards_trend:", # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    # layout="wide",
    # menu_items={
    #     'Get Help': FAQ_URL,
    #     'Report a bug': BUG_REPORT_URL,
    #     'About': "# This is a header. This is an *extremely* cool app!" # TODO
    # },
    initial_sidebar_state="collapsed"
)

### Main App Logic
PROPUBLICA_API_KEY = st.secrets["PROPUBLICA_API_KEY"]
DETA_API_KEY = st.secrets["DETA_API_KEY"]
DETA_ID = st.secrets["DETA_ID"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Chamber
SENATE = 'senate'
HOUSE = 'house'

# ProPublica API
congress = Congress(PROPUBLICA_API_KEY)

### Funcs
@st.cache_data
def get_current_senate_members():
    # https://propublica-congress.readthedocs.io/en/latest/api.html#module-congress.members
    return congress.members.filter(SENATE)[0]["members"]

@st.cache_data
def get_current_house_members():
    # https://propublica-congress.readthedocs.io/en/latest/api.html#module-congress.members
    all_members = congress.members.filter(HOUSE)[0]["members"]
    # Filter only by 50 states
    return [ member for member in all_members if member["state"] in STATE_DICT.keys() ]

@st.cache_data(ttl=60*60*24)
def calculate_age(birthdate):
    today = datetime.now()
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

#@st.cache_data
def render_member(member):
    def set_this_member():
        st.session_state["selected_member"] = member

    container = st.container()
    # Temporary fix for missing image for Senator Pete Ricketts
    if member["id"] == "R000618":
        container.image("https://upload.wikimedia.org/wikipedia/commons/b/bd/Sen._Pete_Ricketts_official_portrait%2C_118th_Congress.jpg", width=200)
    elif "Representative" in member["title"]:
        container.image(f"https://clerk.house.gov/content/assets/img/members/{member['id']}.jpg", width=200)
    elif "Senator" in member["title"]:
        container.image(f"https://www.congress.gov/img/member/{member['id'].lower()}_200.jpg", width=200)
    container.subheader(member["short_title"] + " " + member["first_name"] + " " + member["last_name"])
    #container.text("State: " + STATE_DICT[member["state"]])
    if "district" in member:
        container.text("District: " + member["district"])
    container.text(f"Age: {calculate_age(member['date_of_birth'])}")
    if "next_election" in member:
        container.text("Next Election: " + member["next_election"])
    else:
        container.text("Next Election: N/A")
    if container.button("Voting Record", key=member["id"], on_click = set_this_member):
        switch_page("Voting_Record")

@st.cache_data
def google_geocode_requests(search_address):

    # Set the API endpoint URL and API key
    url = 'https://www.googleapis.com/civicinfo/v2/representatives'

    # Define the API parameters, including the address and API key
    params = {
        'address': search_address,
        'key': GOOGLE_API_KEY
    }

    # Send an HTTP GET request to the API endpoint with the specified parameters
    response = requests.get(url, params=params)

    # Retrieve the JSON response from the API
    response_data = response.json()
    return response_data

@st.cache_data
def search_members(search_by, member):
    '''Returns True if search_by is in member's name, state name, or address'''

    # If search_by is empty, return False
    if not search_by:
        return False
    # Search by name or state
    if search_by.lower() in (member['first_name'] + " " + member['last_name']).lower():
        return True
    elif search_by.lower() in [value.lower() for value in STATE_DICT.values()] and member["state"] in STATE_DICT.keys() and STATE_DICT[member["state"]].lower() == search_by.lower():
        return True
    # Search by address
    else:
        response_data = google_geocode_requests(search_by)
        officials = response_data.get('officials', [])
        if officials:
            for official in officials:
                if (member['first_name'].lower() in official['name'].lower()) and (member['last_name'].lower() in official['name'].lower()):
                    return True

# WEBAPP

if 'senate_members' not in st.session_state:
    st.session_state['senate_members'] = get_current_senate_members()
if 'house_members' not in st.session_state:
    st.session_state['house_members'] = get_current_house_members()

st.markdown("<h1 style='text-align: center;'>Welcome to BillBriefs!</h1>", unsafe_allow_html=True)
st.markdown("---")

#Use USPS API to autofilll address or suggest address
search_by = st.text_input("**Find your Elected Officials.**", placeholder="Search by Name, State, or Address.")

senators_by_state = {}
# Loop for appending senators in session_state to senators_by_state (Sorted by State)
for senator in st.session_state['senate_members']:
    if search_members(search_by, senator):
        state = senator['state']
        if state in STATE_DICT:
            full_state_name = STATE_DICT[state]
            if full_state_name not in senators_by_state:
                senators_by_state[full_state_name] = []
            senators_by_state[full_state_name].append(senator)

reps_by_state = {}
# Loop for appending representatives in session_state to reps_by_state (Sorted by State)
for rep in st.session_state['house_members']:
    if search_members(search_by, rep):
        state = rep['state']
        if state in STATE_DICT:
            full_state_name = STATE_DICT[state]
            if full_state_name not in reps_by_state:
                reps_by_state[full_state_name] = []
            reps_by_state[full_state_name].append(rep)

# If senators_by_state or reps_by_state is not empty, render Members header
if senators_by_state or reps_by_state:
    st.markdown("<h2 style='text-align: center;'>Members</h2>", unsafe_allow_html=True)
    st.markdown("---")

# Loop for rendering senators and representatives by state
for state in sorted(set(senators_by_state.keys()) | set(reps_by_state.keys())):
    with st.expander(f"**{state}**", True):
        # Sets senators equal to senators_by_state for each state
        senators = senators_by_state.get(state, [])
        # Creates two columns for seantors and representatives
        col1, col2 = st.columns(2)
        # If senator 1 exists, render senator 1 in Column 1
        with col1:
            if len(senators) > 0:
                render_member(senators[0])
        # If senator 2 exists, render senator 2 in Column 2
        with col2:
            if len(senators) > 1:
                render_member(senators[1])
        # Sets representatives equal to reps_by_state for each state
        reps = reps_by_state.get(state, [])
        # Sorts representatives by accessnding district number
        sorted_reps = sorted(reps, key=lambda x: (int(x['district']) if 'district' in x and x['district'].isdigit() else 0, x.get('at_large')))
        # Loops through sorted representatives and renders them in alternating columns
        for i, rep in enumerate(sorted_reps):
            # Checks if district is a number
            if 'district' in rep and rep['district'].isdigit():
                # If district is even, render in Column 1
                if i % 2 == 0:
                    with col1:
                        render_member(rep)
                # If district is odd, render in Column 2
                else:
                    with col2:
                        render_member(rep)
            # If district is not a number, render in Column 1
            else:
                with col1:
                    render_member(rep)
                


