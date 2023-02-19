import streamlit as st
import requests
import re
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

@st.cache_data
def google_zipcode_requests(search_zip):
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

    # Set the API endpoint URL and API key
    url = 'https://www.googleapis.com/civicinfo/v2/representatives'

    # Define the API parameters, including the address and API key
    params = {
        'address': search_zip,
        'key': GOOGLE_API_KEY
    }

    # Send an HTTP GET request to the API endpoint with the specified parameters
    response = requests.get(url, params=params)

    # Retrieve the JSON response from the API
    response_data = response.json()
    return response_data

# Search the address for which you want to retrieve representative information
search_zip = st.text_input("Search", placeholder="Search by zipcode")
zip_code_regex = r'\b\d{5}(?:[-\s]\d{4})?\b'
match = re.search(zip_code_regex, search_zip)

if match:
    response_data = google_zipcode_requests(search_zip)

    # Extract the relevant representative information from the response
    officials = response_data['officials']
    offices = response_data['offices']

    # Process and display the representative information
    for office in offices:
        for index in office['officialIndices']:
            official = officials[index]
            st.text('Name: %s, Title: %s' % (official['name'], office['name']))


