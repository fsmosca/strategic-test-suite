"""Shows STS positions with analysis.
"""


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import chess.pgn
from gsheetsdb import connect

from modules.config import Config
from modules.positions import Positions, run_query, get_df, clear_table_cache
from modules.constants import (BOARD_MIN_VALUE, BOARD_MAX_VALUE,
                               BOARD_DEFAULT_VALUE, BOARD_STEP)


# Updates the state variables on all modules.
st.session_state.update(st.session_state)


# Define session states.
if 'myconfig' not in st.session_state:
    st.session_state.myconfig = Config()  # instantiate class

if 'mypos' not in st.session_state:
    st.session_state.mypos = Positions() # instantiate class

if 'conn' not in st.session_state:
    st.session_state.conn = connect()  # instantiate class

if 'board_size_k' not in st.session_state:
    st.session_state.board_size_k = BOARD_DEFAULT_VALUE


st.session_state.myconfig.set_config()
# st.markdown(myconfig.hide_menu(), unsafe_allow_html=True)


def main():
    st.session_state.myconfig.add_logo()

    with st.sidebar.expander('Select Table', expanded=True):
        radio_var = st.radio(
            label='Filtered Table',
            options=['All', 'Reviewed', 'Not yet Reviewed'])

    with st.sidebar.expander('Update Table'):
        st.button('Clear Cache', on_click=clear_table_cache)

    with st.sidebar.expander('Board Size', expanded=False):
        def_board_size = st.session_state.board_size_k
        st.number_input(
            label='Adjust board size',
            min_value=BOARD_MIN_VALUE,
            max_value=BOARD_MAX_VALUE,
            value=def_board_size,
            step=BOARD_STEP,
            key='board_size_k')

    sheet_url = st.secrets["public_gsheets_url"]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    analysis_fn = './data/current_analysis.csv'

    df = pd.DataFrame(rows)
    df_analysis = get_df(analysis_fn)

    df1 = df[['index', 'epd', 'old_bm', 'old_id', 'new_id',
              'comment', 'Reviewed_by', 'Replace', 'Duplicate',
              'unix_sec', 'ferdy_sec']]

    # Create 2 tabs, Data and Analysis hardware.
    tab1, tab2 = st.tabs(['Data', 'Analysis HW'])

    with tab1:

        if radio_var == 'All':
            pass
        elif radio_var == 'Reviewed':
            df1 = df1.loc[~df1['Reviewed_by'].isna()]
        else:
            df1 = df1.loc[df1['Reviewed_by'].isna()]

        grid_table = st.session_state.mypos.get_aggrid_table(df1, 250)
        selected_row = grid_table["selected_rows"]

        cols = st.columns([1, 1])

        if selected_row:
            epd = selected_row[0]['epd']
            test_id = selected_row[0]['old_id']
            board = chess.Board(epd)

            # Show top analysis from epd.
            with cols[1]:
                st.write('#### New analysis')
                df_latest_analysis_1 = df_analysis.loc[df_analysis['epd'] == epd]

                df_latest_analysis_1 = df_latest_analysis_1.drop(
                    ['epd', 'move'], axis=1)
                grid_table_2 = st.session_state.mypos.get_aggrid_table(
                    df_latest_analysis_1, 350)

                selected_row_2 = grid_table_2["selected_rows"]
                if selected_row_2:
                    pv2 = selected_row_2[0]['pv']

            # Show board.
            with cols[0]:
                st.write('#### Board from analysis line')

                fen = board.fen()
                game = chess.pgn.Game()
                game.headers["Result"] = '*'
                game.headers["FEN"] = fen

                if len(df_latest_analysis_1) and len(selected_row_2):
                    node = game
                    for m in pv2.split():
                        node = node.add_main_variation(chess.Move.from_uci(m))

                with st.container():
                    width = st.session_state.board_size_k + 200
                    height = st.session_state.board_size_k + 20
                    components.html(
                        st.session_state.mypos.tempo_html_string(game, board.turn),
                        width=width,
                        height=height,
                        scrolling=True)

                    epd_stdev = None
                    if len(df_latest_analysis_1):
                        epd_stdev = df_latest_analysis_1['eval'].std()
                        epd_stdev = int(round(epd_stdev, 0))

                    st.markdown(f'''
                    Theme: **{test_id}**  
                    Eval stdev: **{epd_stdev}**
                    ''')

    with tab2:
        data_hw = [['unix', 'AMD 5950x 32t 16gb hash'], ['ferdy', 'i7-2600 4t 512mb hash']]
        df_hw = pd.DataFrame(data_hw, columns = ['username', 'analysis setting'])
        st.dataframe(df_hw)


if __name__ == '__main__':
    main()
