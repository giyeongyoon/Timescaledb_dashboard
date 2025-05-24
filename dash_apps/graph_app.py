# dashboard/dash_apps/latest_graph.py
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("🌱 TimescaleDB Dashboard", href="/", className="ms-2"),

        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("최신 데이터", href="/latest", external_link=True)),
                dbc.NavItem(dbc.NavLink("그래프", href="/graph", external_link=True)),
            ],
            className="ms-auto",  # 오른쪽 정렬
            navbar=True
        )
    ]),
    color="dark",
    dark=True,
    sticky="top"
)

body = html.Div(
    [
        dbc.Row([
            dbc.Col([
                html.Label("센서 선택",
                           style={
                               "margin-top": "1.5em",
                               "margin-left": "3em",
                               "font-weight": "bold",
                               "font-size": "1rem"
                           }),
                dcc.Dropdown(
                    options=[
                        {"label": "토양수분", "value": "Teros10"}
                    ],
                    value="Teros10",
                    id="dropdown",
                    style={"margin-left": "1.5em"}
                )
            ], width=3)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="graph")
            ])
        ]),
        dcc.Interval(id="update-interval", interval=10000, n_intervals=0)
    ]
)

def init_graph_dash(server, conn):
    dash_app = Dash(__name__, 
                    server=server, 
                    external_stylesheets=[dbc.themes.BOOTSTRAP], 
                    url_base_pathname="/graph/")
    
    dash_app.layout = html.Div(
        [
            navbar,
            body
        ]
    )

    @dash_app.callback(
        Output("graph", "figure"),
        [Input("dropdown", "value"),
        Input("update-interval", "n_intervals"),
        Input("graph", "relayoutData")]
    )
    def get_graph(value, n, relayout_data):
        sql = """
            SELECT time AT TIME ZONE 'Asia/Seoul' AS local_time, moisture \
            FROM soil_moisture
            WHERE time > now() - interval '10 minutes'
            ORDER BY time ASC;
        """

        df = pd.read_sql(sql, conn)
        fig = go.Figure(data=go.Scatter(x=df['local_time'],
                                        y=list(df['moisture'].values),
                                        mode='lines'))
        fig.update_layout(
            title = {'text': f'Sensor: {value}',
                    'x': 0.5},
            xaxis_title="Time",
            yaxis_title="Moisture (%)",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1h", step="hour", stepmode="backward"),
                        dict(count=6, label="6h", step="hour", stepmode="backward"),
                        dict(count=1, label="1d", step="day", stepmode="backward"),
                        dict(step="all", label="전체 보기")
                    ])
                ),
                type="date",
                rangeslider=dict(visible=True)
            ),
            yaxis=dict(range=[0, 64]),
            margin=dict(t=50, l=50, r=50, b=50))
        
        if relayout_data and "xaxis.range[0]" in relayout_data:
            fig.update_layout(xaxis_range=[
                relayout_data["xaxis.range[0]"],
                relayout_data["xaxis.range[1]"]
            ])
                        

        return fig
    
    return dash_app