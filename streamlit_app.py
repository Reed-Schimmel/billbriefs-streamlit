import streamlit as st
from congress import Congress
from dotenv import load_dotenv, dotenv_values
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
env_config = dotenv_values(".env")
PROPUBLICA_API_KEY = env_config["PROPUBLICA_API_KEY"]
DETA_API_KEY = env_config["DETA_API_KEY"]
DETA_ID = env_config["DETA_ID"]

# Chamber
SENATE = 'senate'
HOUSE = 'house'


st.write("I want to summize the voting records for each member of congress using GPT and ProPublica")
st.write(env_config)
