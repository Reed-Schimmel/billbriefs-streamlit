import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from bs4 import BeautifulSoup

from datetime import datetime#, timedelta

from congress_funcs import build_voting_records, get_bill, get_bill_summaries_official, validate_bill_id
from utils import html_to_structured_text
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
st.write(st.session_state["selected_member"])
'''
Now what I must do is filter by positions that passed.
Then by actual bills (not all votes are on bills).
Then grab the summary or title/short title for each bill (hopefully already cached)
I will display a list of "date, bill_id, position" then expand for text.

'''
st.subheader("Voting Positions by vote result")

chamber = SENATE if "Senator" in st.session_state["selected_member"]["title"] else HOUSE
all_voting_positions = build_voting_records(chamber, datetime(2022, 5, 1, 0, 0, 0))
member_voting_positions = all_voting_positions[st.session_state["selected_member"]['id']]

with st.expander("Positions"):
    result_filter = st.selectbox("Vote Result", member_voting_positions.keys())
    selected_positions = [vp for vp in member_voting_positions[result_filter] if validate_bill_id(vp['bill_id'])]
    show_cols = st.multiselect("Render Columns", selected_positions[0].keys(), default=selected_positions[0].keys())
    df = pd.DataFrame(selected_positions)
    df = df.sort_values(['bill_id', 'date'])
    st.table(df[show_cols])

###################

st.header("Bill Summary")
# st.write(df['bill_id'].unique())
bill_id = st.selectbox('bill_id', df['bill_id'].unique())

#validate bill_id, must have the form <bill_type><bill_number>-<congress_number>


st.subheader("ProPub details")
bill_deets = get_bill(bill_id)
if bill_deets is not None:
    text_fields = ["title","short_title","summary","summary_short",]
    for field in text_fields:
        st.text(field)
        st.write(bill_deets[field])

st.subheader("Official details")
off_deets = get_bill_summaries_official(bill_id)
# if off_deets is not None:
#     # st.write(off_deets)
#     text_data = off_deets['summaries'][0]['text']
#     soup = BeautifulSoup(text_data, "html.parser")
#     st.write(soup.get_text())
#     st.write(text_data)
st.caption("Pretty text")
html_string = off_deets['summaries'][0]['text']
st.write(html_to_structured_text(html_string))

st.caption("Raw text")
st.write(html_string)



# {
# "bill_id":"hr1123-118"
# "date":"2023-03-07"
# "time":"14:16:00"
# "vote_position":"Yes"
# "chamber":"House"
# "rollcall_num":133
# "session":1
# "congress":118
# }