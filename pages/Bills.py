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
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Chamber
SENATE = 'senate'
HOUSE = 'house'

# ProPublica API
congress = Congress(PROPUBLICA_API_KEY)

st.title("ProPublica Bill Viewer")
bill_type = st.selectbox("Type of bills to search for.", ["Passed"])#, "By Member"])
chamber = st.selectbox("Chamber", [HOUSE, SENATE])
congress_num = st.number_input("Congress number (Current 118)", min_value=110, max_value=118, value=117)


@st.cache_data
def get_bills(bill_type, chamber, congress_num):
    if bill_type == "Passed":
        return congress.bills.passed(chamber=chamber, congress=congress_num)
    # if bill_type == "By Member":
    #     return congress.bills.by_member(chamber=chamber, congress=congress_num)

if st.button("Search"):
    data = get_bills(bill_type, chamber, congress_num)
    st.write(data)
