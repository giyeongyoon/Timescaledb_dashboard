# dashboard/dash_apps/latest_app.py
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("🌱 TimescaleDB Dashboard", href="/", className="ms-2"),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("최신 데이터", href="/latest", external_link=True)),
                    dbc.NavItem(dbc.NavLink("그래프", href="/graph", external_link=True)),
                ],
                className="ms-auto",
                navbar=True,
            ),
            id="navbar-collapse",
            is_open=False,
            navbar=True
        ),
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
                    html.H3(id="moisture-value", className="text-primary text-center fw-bold"),
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
        sql = """SELECT time AT TIME ZONE 'Asia/Seoul' AS local_time, moisture 
        FROM soil_moisture 
        ORDER BY time DESC 
        LIMIT 1;"""
        df = pd.read_sql(sql, conn)

        if df.empty:
            return "데이터 없음", ""
        value = f"{df['moisture'].iloc[0]:.2f} %"
        timestamp = df['local_time'].iloc[0].strftime('%Y-%m-%d %H:%M:%S')
        return value, timestamp
    
    # Navbar toggle callback
    @dash_app.callback(
        Output("navbar-collapse", "is_open"),
        Input("navbar-toggler", "n_clicks"),
        State("navbar-collapse", "is_open")
    )
    def toggle_navbar(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

    return dash_app