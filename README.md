# [ProPublica Data Store](https://www.propublica.org/datastore/apis)
- [Congress API](https://www.propublica.org/datastore/api/propublica-congress-api)
    - [Docs](https://projects.propublica.org/api-docs/congress-api/)
    - [Python Lib](https://github.com/eyeseast/propublica-congress) - [Docs](https://propublica-congress.readthedocs.io/en/latest/)
- [Streamlit Extras](https://github.com/arnaudmiribel/streamlit-extras)

## Setup
1. clone this repo
1. cd in dir
1. `conda create -n [envname] python=3.10`
1. `conda activate [envname]`
1. `pip install -r requirements.txt`
1. Add your API keys to `.streamlit/secrets.toml`. Create the file if needed.

## Run
`streamlit run streamlit_app.py`

## Notes
- app secrets https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management

## App Flow for voters
1. input zipcode
1. app get's applicable members
1. app get all bills during member tenor
1. GPT summarizes all bills to 1 liner
1. user swipes on one-liners (support, oppose, or skip)
1. app shows the alignment of the voter with members up for re-election

Call it elective review

Future ideas: some members might be coming back to challenge the current person. Take their past voting records. Still no idea how to handle complete noobs.