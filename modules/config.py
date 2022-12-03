import streamlit as st


class Config:
    def __init__(self):
        pass

    def set_config(self):
        st.set_page_config(
            page_title="STS - Strategic Test Suite",
            page_icon="🏆",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://github.com/fsmosca/strategic-test-suite',
                'Report a bug': "https://github.com/fsmosca/strategic-test-suite/issues",
                'About': "An engine test suite to determine its position strategic understanding."
            }
        )

    def hide_menu(self):
        hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
        return hide_menu_style

    def add_logo(self):
        st.markdown(
            """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url(https://lh4.googleusercontent.com/vtzDjXM6oK90eR3KkwpcUls89dvppljcSKxSAAsg3YCRQOIhGiC3WDEZYefPcMvH-HtG2Q=w16383);
                    background-repeat: no-repeat;
                    padding-top: 10px;
                    background-position: 20px 20px;
                }
                [data-testid="stSidebarNav"]::before {
                    content: "STS - Strategic Test Suite";
                    margin-left: 20px;
                    margin-top: 20px;
                    font-size: 15px;
                    position: relative;
                    top: 80px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
