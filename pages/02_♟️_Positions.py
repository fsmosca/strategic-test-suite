"""Shows STS positions with analysis.
"""


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import chess.pgn

from modules.config import Config
from modules.positions import Positions


myconfig = Config()
mypos = Positions()

myconfig.set_config()
# st.markdown(myconfig.hide_menu(), unsafe_allow_html=True)


@st.experimental_memo
def get_df(fn):
    return pd.read_csv(fn)


def main():
    myconfig.add_logo()

    radio_var = st.sidebar.radio(label='', options=['All', 'Reviewed', 'Not yet Reviewed'])

    table_fn = './data/sts_positions - stockfish 15.csv'
    analysis_fn = './data/current_analysis.csv'

    df = get_df(table_fn)
    df_analysis = get_df(analysis_fn)

    df1 = df[['index', 'epd', 'old bm', 'old id', 'new id',
              'comment', 'Reviewed by', 'Replace']]

    if radio_var == 'All':
        grid_table = mypos.get_aggrid_table(df1, 250)
    elif radio_var == 'Reviewed':
        df1 = df1.loc[~df1['Reviewed by'].isna()]
        grid_table = mypos.get_aggrid_table(df1, 250)
    else:
        df1 = df1.loc[df1['Reviewed by'].isna()]
        grid_table = mypos.get_aggrid_table(df1, 250)

    selected_row = grid_table["selected_rows"]

    cols = st.columns([1, 1])

    if selected_row:
        epd = selected_row[0]['epd']
        test_id = selected_row[0]['old id']
        board = chess.Board(epd)

        # Show top analysis from epd.
        with cols[1]:
            st.write('#### New analysis')
            df_latest_analysis_1 = df_analysis.loc[df_analysis['epd'] == epd]

            df_latest_analysis_1 = df_latest_analysis_1.drop(['epd', 'move'], axis=1)
            grid_table_2 = mypos.get_aggrid_table(df_latest_analysis_1, 350)

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
                components.html(
                    mypos.tempo_html_string(game, board.turn),
                    width=450,
                    height=270,
                    scrolling=True)

                epd_stdev = None
                if len(df_latest_analysis_1):
                    epd_stdev = df_latest_analysis_1['eval'].std()

                st.markdown(f'''
                Theme: **{test_id}**  
                Eval stdev: **{int(round(epd_stdev, 0)) if epd_stdev is not None else None}**
                ''')
    

if __name__ == '__main__':
    main()
