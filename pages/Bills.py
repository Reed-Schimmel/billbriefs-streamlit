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
BOTH = 'both'


@st.cache_data
def download_all_passed_bills(congress_num, chamber, verbose=False):
    bills = []

    page=1
    passed_bills = congress.bills.passed(chamber=chamber, congress=congress_num, page=1)
    while passed_bills['num_results'] > 0:
        if verbose:
            print(f"{len(bills)} downloaded")

        bills.extend(passed_bills['bills'])
        page += 1
        passed_bills = congress.bills.passed(chamber=chamber, congress=congress_num, page=page)

    if verbose:
        print(f"{len(bills)} bills downloaded from {bills[-1]['last_vote']} to {bills[0]['last_vote']}")
    return bills



# ProPublica API
congress = Congress(PROPUBLICA_API_KEY)

st.title("ProPublica Bill Viewer")
bill_type = st.selectbox("Type of bills to search for.", ["Passed"])#, "By Member"])
chamber = st.selectbox("Chamber", [BOTH, HOUSE, SENATE])
congress_num = st.number_input("Congress number (Current 118)", min_value=110, max_value=118, value=117)




if st.button("Search"):
    if bill_type == "Passed":
        data = download_all_passed_bills(congress_num, chamber)
        st.write(data[:20])
