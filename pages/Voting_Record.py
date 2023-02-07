import streamlit as st
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

st.title("Voting Record")

if st.button("Go Back"):
    st.session_state["selected_member"] = None
    switch_page("Member_List")

st.write(st.session_state["selected_member"])