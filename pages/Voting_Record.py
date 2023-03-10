import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from datetime import datetime#, timedelta

from congress_funcs import build_voting_records
from const import HOUSE, SENATE

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

PROPUBLICA_API_KEY = st.secrets["PROPUBLICA_API_KEY"]

# If session state is empty, go to home.
if len(st.session_state) == 0:
    switch_page("streamlit app")
elif "selected_member" not in st.session_state:
    switch_page("streamlit app")

st.title("Voting Record")

if st.button("Go Back"):
    st.session_state["selected_member"] = None
    switch_page("Member_List")

############################## HERE YA GO #########################################
st.subheader("Voting Positions on Bills that passed.")

st.write(st.session_state["selected_member"])
chamber = SENATE if "Senator" in st.session_state["selected_member"]["title"] else HOUSE
all_voting_positions = build_voting_records(chamber, datetime(2022, 5, 1, 0, 0, 0))
st.write(all_voting_positions[st.session_state["selected_member"]['id']])

