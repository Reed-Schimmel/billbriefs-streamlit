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
        container.image(f"https://www.congress.gov/img/member/{member['id'].lower()}_200.jpg")
    container.subheader(member["short_title"] + " " + member["first_name"] + " " + member["last_name"])
    #container.text("State: " + STATE_DICT[member["state"]])
    if "district" in member:
        container.text("District: " + member["district"])
    container.text(f"Age: {calculate_age(member['date_of_birth'])}")
    if "next_election" in member:
        container.text("Next Election: " + member["next_election"])
    if container.button("Voting Record", key=member["id"], on_click = set_this_member):
        switch_page("Voting_Record")

@st.cache_data
def google_geocode_requests(search_address):
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

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

    # Search by name or state
    if search_by.lower() in (member['first_name'] + " " + member['last_name']).lower():
        return True
    elif search_by.lower() in [value.lower() for value in STATE_DICT.values()] and member["state"] in STATE_DICT.keys() and STATE_DICT[member["state"]].lower() == search_by.lower():
        return True

    response_data = google_geocode_requests(search_by)
    officials = response_data.get('officials', [])
    if officials:
        for official in officials:
            if (member['first_name'].lower() in official['name'].lower()) and (member['last_name'].lower() in official['name'].lower()):
                return True

    return False

# WEBAPP

if 'senate_members' not in st.session_state:
    st.session_state['senate_members'] = get_current_senate_members()
if 'house_members' not in st.session_state:
    st.session_state['house_members'] = get_current_house_members()

st.markdown("<h1 style='text-align: center;'>Welcome to BillBriefs!</h1>", unsafe_allow_html=True)
st.markdown("---")

search_by = st.text_input("**Find your Elected Officials**", placeholder="Search by name, state, or address.")

st.markdown("<h2 style='text-align: center;'>Members</h2>", unsafe_allow_html=True)
st.markdown("---")

senators_by_state = {}
reps_by_state = {}

for senator in st.session_state['senate_members']:
    if search_members(search_by, senator):
        state = senator['state']
        if state in STATE_DICT:
            full_state_name = STATE_DICT[state]
            if full_state_name not in senators_by_state:
                senators_by_state[full_state_name] = []
            senators_by_state[full_state_name].append(senator)

for rep in st.session_state['house_members']:
    if search_members(search_by, rep):
        state = rep['state']
        if state in STATE_DICT:
            full_state_name = STATE_DICT[state]
            if full_state_name not in reps_by_state:
                reps_by_state[full_state_name] = []
            reps_by_state[full_state_name].append(rep)

for state in sorted(set(senators_by_state.keys()) | set(reps_by_state.keys())):
    with st.expander(f"**{state}**", True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: left;'>Senators</h3>", unsafe_allow_html=True)
            for senator in senators_by_state.get(state, []):
                render_member(senator)
        with col2:
            st.markdown("<h3 style='text-align: left;'>Representatives</h3>", unsafe_allow_html=True)
            reps = reps_by_state.get(state, [])
            sorted_reps = sorted(reps, key=lambda x: (int(x['district']) if 'district' in x and x['district'].isdigit() else 0))
            for rep in sorted_reps:
                render_member(rep)