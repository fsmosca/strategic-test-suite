import streamlit as st
from modules.config import Config
from modules.constants import BOARD_DEFAULT_VALUE


# Define session states.
if 'myconfig' not in st.session_state:
    st.session_state.myconfig = Config()  # instantiate class

st.session_state.myconfig.set_config()

# Updates the state variables on all modules.
st.session_state.update(st.session_state)

if 'board_size_k' not in st.session_state:
    st.session_state.board_size_k = BOARD_DEFAULT_VALUE


def main():
    st.session_state.myconfig.add_logo()

    st.markdown(f'''
    ## STS - Strategic Test Suite
    Official site: https://sites.google.com/site/strategictestsuite/
    ''')


if __name__ == '__main__':
    main()
