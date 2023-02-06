import streamlit as st
from congress import Congress
from datetime import datetime, timedelta

from const import STATE_DICT

# Config webapp
st.set_page_config(
    # page_title="Best TA Demo",
    # page_icon=":chart_with_upwards_trend:", # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
    # layout="wide",
    # menu_items={
    #     'Get Help': FAQ_URL,
    #     'Report a bug': BUG_REPORT_URL,
    #     'About': "# This is a header. This is an *extremely* cool app!" # TODO
    # },
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
    return congress.members.filter(HOUSE)[0]["members"]

@st.cache(ttl=60*60*24)
def calculate_age(birthdate):
    today = datetime.now()
    birthdate = datetime.strptime(birthdate, '%Y-%m-%d')
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def render_member(member):
    container = st.container()
    container.image(f"https://www.congress.gov/img/member/{member['id'].lower()}_200.jpg")
    container.subheader(member["short_title"] + " " + member["first_name"] + " " + member["last_name"])
    container.text("State: " + STATE_DICT[member["state"]])
    if "district" in member:
        container.text("District: " + member["district"])
    container.text(f"Age: {calculate_age(member['date_of_birth'])}")
    container.text("Next Election: " + member["next_election"])
    container.button("Voting Record", key=member["id"])
    
# WEBAPP
# st.write("I want to summize the voting records for each member of congress using GPT and ProPublica")

st.title("Members")
st.header("Senate")
senate_members = get_current_senate_members()
#st.write(senate_members)
for senator in senate_members[:5]:
    render_member(senator)
st.header("House")
house_members = get_current_house_members()
for rep in house_members[:5]:
    render_member(rep)
#st.write(house_members)