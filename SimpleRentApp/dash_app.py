import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


# create dash application
def create_dash_app(server):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    dash_app = dash.Dash(__name__,
                         server=server,
                         routes_pathname_prefix='/dash/',
                         external_stylesheets=[
                             external_stylesheets, dbc.themes.BOOTSTRAP]
                         )

    # load data
    data = pd.read_csv("SimpleRentApp/rent_rates_data.csv")

    # create town summary
    town_summary = data.groupby(['town', 'bedrooms'])['price'].mean().round(
        0).reset_index().sort_values(by=['town', 'bedrooms'])
    town_summary.columns = ['town', 'bedrooms', 'avg_price']

    # print(town_summary)

    # define app layout
    dash_app.layout = html.Div([
        # dbc.Row([
            html.Div([
                html.H2("Rent Prices In Kenya's Major Towns")
            ],style = {'width':'100%','float':'center','display':'block'}),
        # ]),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id="selected_town",
                    options=[{'label': x, 'value': x}
                             for x in sorted(town_summary['town'].unique())],
                    value=town_summary['town'].unique()[np.random.randint(low=1,
                                                                          high=len(town_summary['town'].unique()))],
                    placeholder="Select town ...",
                    multi=True
                ),
                width={"size": 3, "offset": 0}),
            dbc.Col(
                dcc.Graph(
                    id="main_graph",
                    # figure=fig
                ),
              )
        ])
    ])
    
    # update graph based
    # based on town selection
    @dash_app.callback(
        Output('main_graph', 'figure'),
        [Input('selected_town', 'value')])
    # define function to update graph
    def update_main_graph(town_list):
        
        # create an empty dataframe
        df = pd.DataFrame()
        try:
            df = town_summary[town_summary['town'] == town_list]
        except:
            for i in town_list:
                df_filter = town_summary[town_summary['town'] == i]
                df = pd.concat([df, df_filter])

        # print(df)

        # plot distribution
        fig = px.bar(df, x='bedrooms', y='avg_price', color='town',
                     hover_data=['avg_price'], hover_name='town', barmode='group',
                     labels={
                         'avg_price': 'Price (Ksh)', 'bedrooms': 'Bedrooms', 'town': 'Town'},
                     width=800, height=500)
        fig.update_layout(transition_duration=500)
        fig.update_layout(title = {
                              'text' :'Average Rent Price / Bedroom',
                              'x':0.5,
                              'y':0.95,
                              'xanchor' :'center',
                              'yanchor' :'top'
                              })

        return fig

    return dash_app.server
