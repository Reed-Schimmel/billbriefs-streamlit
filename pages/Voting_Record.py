import streamlit as st
import congress
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

tree = ET.parse("roll_call_votes.xml")
root = tree.getroot()

congress_num = root.find("./vote-metadata/congress").text
legis_num = root.find("./vote-metadata/legis-num").text
rollcall_num = root.find("./vote-metadata/rollcall-num").text

vote_data = []
for recorded_vote in root.findall("./vote-data/recorded-vote"):
    id = recorded_vote.find("./legislator").attrib["name-id"]
    vote = recorded_vote.find("./vote").text
    if id == selected_member:
        st.text("Congress: {}  Legislation: {}  Roll Call: {}  Vote: {}".format(congress_num, legis_num, rollcall_num, vote))
        break



