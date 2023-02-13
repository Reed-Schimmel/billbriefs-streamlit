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
selected_member = st.session_state["selected_member"]["id"]

rollcall_number = 1

while True:
    formatted_rollcall_number = str(rollcall_number).zfill(3)
    url = "https://clerk.house.gov/evs/2023/roll" + formatted_rollcall_number + ".xml"
    response = requests.get(url)
    if response.status_code == 404:
        break
    xml_string = response.content

    root = ET.fromstring(xml_string)

    congress_num = root.find("./vote-metadata/congress").text
    rollcall_num = root.find("./vote-metadata/rollcall-num").text
    legis_num = root.find("./vote-metadata/legis-num")
    if legis_num is not None:
        legis_num = legis_num.text
    vote_question = root.find("./vote-metadata/vote-question").text
    vote_result = root.find("./vote-metadata/vote-result").text

    vote_data = []
    for recorded_vote in root.findall("./vote-data/recorded-vote"):
        id = recorded_vote.find("./legislator").attrib["name-id"]
        vote = recorded_vote.find("./vote").text
        if id == selected_member:
            st.text("Congress: {}  Roll Call: {}  Legislation: {}  Vote Question: {}  Vote Result: {}  Vote: {}".format(congress_num, rollcall_num, legis_num, vote_question, vote_result, vote))
            break

    rollcall_number += 1



