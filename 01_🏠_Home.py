import streamlit as st
from modules.config import Config


myconfig = Config()
myconfig.set_config()


def main():
    myconfig.add_logo()

    st.markdown(f'''
    ## STS - Strategic Test Suite
    Official site: https://sites.google.com/site/strategictestsuite/
    ''')


if __name__ == '__main__':
    main()
