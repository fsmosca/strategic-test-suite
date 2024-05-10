import streamlit as st
import pandas as pd


st.set_page_config(
    layout='centered',
    page_title="STS - Strategic Test Suite",
    page_icon="🏆",
)

try:
    st.session_state.myconfig.add_logo()
except AttributeError:
    st.switch_page('01_🏠_Home.py')

st.markdown(
    '''
    # 🗃️📂 Download
    '''
    )    

with open("./static/sts_v8.epd", "r") as file:
    st.download_button(
        label="🔥 Download STS Positions in epd format",
        data=file,
        file_name="sts_v8.epd",
        mime="text/epd"
    )
