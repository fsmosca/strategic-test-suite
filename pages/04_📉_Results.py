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


@st.cache_data
def get_results():
    df = pd.read_csv('./static/sts_results.csv')

    return df


st.markdown(
    '''
    # 📉 Test results
    '''
    )  

st.markdown(
    '''
    sts_v8.epd is used to test the engines. This is from STS Positions analyzed with sf15 and sf16.1 but mostly sf15.
    The mtms is the movetime in milliseconds.

    You can download the test set in the Download page.
    '''
    )
df = get_results()
st.dataframe(df, use_container_width=True, hide_index=True)
