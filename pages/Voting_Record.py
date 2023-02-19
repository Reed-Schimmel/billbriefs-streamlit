import streamlit as st
import requests
import xml.etree.ElementTree as ET
from streamlit_extras.switch_page_button import switch_page

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
st.write(st.session_state["selected_member"])



