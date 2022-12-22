"""Shows STS positions with analysis.
"""


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import chess.pgn
from shillelagh.backends.apsw.db import connect
import plotly.express as px

from modules.config import Config
from modules.positions import (Positions, run_query, get_df,
                               clear_table_cache, theme_names)
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
    st.session_state.conn = connect(":memory:")

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
        st.button('Update data', on_click=clear_table_cache, help='Pull new data from google sheet.')

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
    query = f'SELECT * FROM "{sheet_url}"'
    df = run_query(query)

    sheet_analysis = st.secrets["public_sheets_analysis"]
    query = f'SELECT * FROM "{sheet_analysis}"'
    df_analysis = run_query(query)

    df1 = df[['index', 'epd', 'old_bm', 'old_id', 'new_id',
              'comment', 'Reviewed_by', 'Replace', 'Duplicate',
              'unix_sec', 'ferdy_sec']]

    # Create tabs
    tab1, tab2, tab3 = st.tabs(['Data', 'Theme Names', 'Analysis HW'])

    # Data for pie chart.
    check_count = len(df1.loc[~df1['Reviewed_by'].isna()])
    not_check_count = len(df1.loc[df1['Reviewed_by'].isna()])
    prog_df = pd.DataFrame({'cat': ['check', 'not check'],
                            'value': [check_count, not_check_count]})

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

        cols = st.columns([1, 1, 1])

        with cols[0]:
            with st.expander('Check Progress', expanded=False):
                fig = px.pie(prog_df, values='value', names='cat', title='Checking progress',
                             height=200, width=200)
                fig.update_layout(
                    margin=dict(l=20, r=20, t=30, b=0),)
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        df_themes = theme_names()
        st.dataframe(df_themes)

    with tab3:
        data_hw = [['unix', 'AMD Ryzen 9 5950x, 16 cores / 32 threads'],
                   ['ferdy', 'i7-2600 4 cores / 8 threads'],
                   ['criko', 'AMD Ryzen Threadripper PRO 3995WX, 64 core / 128 threads']]
        df_hw = pd.DataFrame(data_hw, columns = ['username', 'analysis setting'])
        df_hw = df_hw.sort_values(by=['username'], ascending=[True])
        df_hw = df_hw.reset_index(drop=True)
        st.dataframe(df_hw)


if __name__ == '__main__':
    main()
