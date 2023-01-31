import streamlit as st
from congress import Congress

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
    return congress.members.filter(SENATE)[0]["members"]

@st.cache
def get_current_house_members():
    return congress.members.filter(HOUSE)[0]["members"]

# WEBAPP
st.write("I want to summize the voting records for each member of congress using GPT and ProPublica")

st.header("Members")
# https://propublica-congress.readthedocs.io/en/latest/api.html#module-congress.members
senate_members = get_current_senate_members()
house_members = get_current_house_members()
st.write(senate_members[0])