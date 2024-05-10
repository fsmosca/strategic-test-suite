import streamlit as st
import pandas as pd


st.set_page_config(
    layout='centered',
    page_title="STS - Strategic Test Suite",
    page_icon="🏆",
)


@st.cache_data
def get_sts_table():
    df = pd.read_csv('./static/sts_v8.csv')

    return df


st.markdown(
    '''
    # 🗃️📂 Download files
    '''
    )    

with open("./static/sts_v8.epd", "r") as file:
    st.download_button(
        label="🔥 Download STS Positions in epd format",
        data=file,
        file_name="sts_v8.epd",
        mime="text/epd"
    )

st.markdown(
    '''STS Positions mostly analyzed with sf15 and sf16. The field "c7" contains the top n moves of the positions
    with corresponding points in "c8" field.
    ''')

df = get_sts_table()
st.dataframe(df, width=400, use_container_width=True, hide_index=True)
