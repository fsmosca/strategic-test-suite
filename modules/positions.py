"""Handles functionalities in pages/positions.py.
"""


import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
from shillelagh.backends.apsw.db import connect


class Positions:
    def __init__(self):
        pass

    def get_aggrid_table(self, df, height=300, use_box=True):
        """Displays df using aggrid."""
        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_default_column(
            editable=True, groupable=False)
        gd.configure_selection(
            selection_mode='single', use_checkbox=use_box,
            pre_selected_rows=[0], suppressRowDeselection=True)
        gridoptions = gd.build()
        grid_table = AgGrid(
            df, height=height, gridOptions=gridoptions,
            theme='streamlit',
            fit_columns_on_grid_load=True,
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


@st.cache_resource
def run_query(query):
    """Perform SQL query on the Google Sheet."""
    cursor = st.session_state.conn.cursor()
    rows = cursor.execute(query)
    df = pd.DataFrame(rows)
    df.columns = ['index', 'epd', 'old_bm', 'sts_v6', 'old_id', 'new_id', 'test', 
              'depth', 'by', 'status', 'date', 'output_file', 'updated_by',
              'update_date', 'update_depth', 'epd_index_check', 'comment',
              'Reviewed_by', 'Replace', 'Duplicate',
              'unix_sec', 'ferdy_sec']
    
    return df


@st.cache_resource
def run_query_analysis(query):
    """Perform SQL query on the Google Sheet."""
    cursor = st.session_state.conn.cursor()
    rows = cursor.execute(query)
    df = pd.DataFrame(rows)
    df.columns = ['epd','move','eval','depth','pv','engine']
    
    return df


@st.cache_data
def get_df(fn):
    return pd.read_csv(fn)


def clear_table_cache():
    run_query.clear()
    run_query_analysis.clear()


def theme_names():
    """Gets the dataframe of theme"""
    themes = [['STS 01', 'Undermining'], ['STS 02', 'Open Files and Diagonals'],
              ['STS 03', 'Knight Outposts'], ['STS 04', 'Square Vacancy'],
              ['STS 05', 'Bishop vs Knight'], ['STS 06', 'Re-Capturing'],
              ['STS 07', 'Offer of Simplification'], ['STS 08', 'Advancement of f/g/h Pawns'],
              ['STS 09', 'Advancement of a/b/c Pawns'], ['STS 10', 'Simplification'],
              ['STS 11', 'Activity of the King'], ['STS 12', 'Center Control'],
              ['STS 13', 'Pawn Play in the Center'], ['STS 14', 'Queens and Rooks to the 7th rank'],
              ['STS 15', 'Avoid Pointless Exchange']
             ]
    df = pd.DataFrame(themes)
    df.columns = ['Id', 'Name']

    return df
    