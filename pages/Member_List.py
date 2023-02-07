import streamlit as st
from congress import Congress
from datetime import datetime, timedelta
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

# Chamber
SENATE = 'senate'
HOUSE = 'house'

# ProPublica API
congress = Congress(PROPUBLICA_API_KEY)


### Funcs
@st.cache
def get_current_senate_members():
    # https://propublica-congress.readthedocs.io/en/latest/api.html#module-congress.members
    return congress.members.filter(SENATE)[0]["members"]

@st.cache
def get_current_house_members():
    # https://propublica-congress.readthedocs.io/en/latest/api.html#module-congress.members
    all_members = congress.members.filter(HOUSE)[0]["members"]
    # Filter only by 50 states
    return [ member for member in all_members if member["state"] in STATE_DICT.keys() ]

@st.cache(ttl=60*60*24)
def calculate_age(birthdate):
    today = datetime.now()
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def render_member(member):
    def set_this_member():
        st.session_state["selected_member"] = member

    container = st.container()
    container.image(f"https://www.congress.gov/img/member/{member['id'].lower()}_200.jpg")
    container.subheader(member["short_title"] + " " + member["first_name"] + " " + member["last_name"])
    container.text("State: " + STATE_DICT[member["state"]])
    if "district" in member:
        container.text("District: " + member["district"])
    container.text(f"Age: {calculate_age(member['date_of_birth'])}")
    if "next_election" in member:
        container.text("Next Election: " + member["next_election"])
    if container.button("Voting Record", key=member["id"], on_click = set_this_member):
        switch_page("Voting_Record")


# WEBAPP
st.title("Members")
st.markdown("---")

st.header("Senate")
senate_members = get_current_senate_members()
with st.expander("State Senators", True):
    for senator in senate_members:
        render_member(senator)

st.header("House")
house_members = get_current_house_members()
with st.expander("State Representatives", True):
    for rep in house_members:
        render_member(rep)