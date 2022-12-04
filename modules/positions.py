"""Handles functionalities in pages/positions.py.
"""


import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd


class Positions:
    def __init__(self):
        pass

    def get_aggrid_table(self, df, height=300, use_box=True):
        """Displays df using aggrid."""
        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_default_column(
            min_column_width=5, editable=True, groupable=False)
        gd.configure_selection(
            selection_mode='single', use_checkbox=use_box,
            pre_selected_rows=[0], suppressRowDeselection=True)
        gridoptions = gd.build()
        grid_table = AgGrid(
            df, height=height, gridOptions=gridoptions,
            enable_enterprise_modules=False)
        return grid_table

    def tempo_html_string(self, game, turn):
        """Build game with diagram."""
        html_string = f'''
        <head>
        <link href="https://c2a.chesstempo.com/pgnviewer/v2.5/pgnviewerext.vers1.css" media="all" rel="stylesheet" crossorigin>
        <script defer language="javascript" src="https://c1a.chesstempo.com/pgnviewer/v2.5/pgnviewerext.bundle.vers1.js" crossorigin></script>
        <link
        href="https://c1a.chesstempo.com/fonts/MaterialIcons-Regular.woff2"
        rel="stylesheet" crossorigin>
        </head>
        <body>
        <ct-pgn-viewer board-size={st.session_state.board_size_k}px
          move-list-folding=false
          move-list-resizable=false board-resizable=false
          move-list-position=right board-coords-style=internal
          buttons-above-moves=true flip={"false" if turn else "true"}>
        {game}
        </ct-pgn-viewer>
        </body>
        '''
        return html_string


@st.experimental_singleton
def run_query(query):
    """Perform SQL query on the Google Sheet."""
    rows = st.session_state.conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


@st.experimental_memo
def get_df(fn):
    return pd.read_csv(fn)


def clear_table_cache():
    run_query.clear()
