# dashboard/dash_apps/latest_app.py
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

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

body = dbc.Container([
    html.H3("최신 센서 측정값", className="my-5 text-center fw-semibold"),

    dcc.Interval(id="interval", interval=10000, n_intervals=0),

    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H6("토양 수분", className="text-muted text-center"),
                    html.H1(id="moisture-value", className="text-primary text-center display-4 fw-bold"),
                    html.P(id="timestamp", className="text-center text-muted small")
                ]),
                className="shadow-sm border-0"
            ),
            width=4, className="mx-auto"
        )
    ])
], fluid=True)

def init_latest_dash(server, conn):
    dash_app = Dash(__name__, 
                    server=server, 
                    external_stylesheets=[dbc.themes.BOOTSTRAP], 
                    url_base_pathname="/latest/")

    dash_app.layout = html.Div(
        [
            navbar,
            body
        ]
    )

    @dash_app.callback(
        [Output("moisture-value", "children"),
        Output("timestamp", "children")],
        [Input("interval", "n_intervals")]
    )
    def update(n):
        sql = "SELECT time, moisture FROM soil_moisture ORDER BY time DESC LIMIT 1;"
        df = pd.read_sql(sql, conn)

        if df.empty:
            return "데이터 없음", ""
        value = f"{df['moisture'].iloc[0]:.2f} %"
        timestamp = df['time'].iloc[0].strftime('%Y-%m-%d %H:%M:%S')
        return value, timestamp
    
    return dash_app