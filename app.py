from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from flask import Flask
from postgresql import get_conn_db
import pandas as pd
import plotly.graph_objects as go


conn = get_conn_db()

app = Flask(__name__)
dash_app1 = Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname="/latest/")
dash_app2 = Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP], url_base_pathname="/graph/")

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

latest_body = dbc.Container([
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

graph_body = html.Div(
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

dash_app1.layout = html.Div(
    [
        navbar,
        latest_body
    ]
)

dash_app2.layout = html.Div(
    [
        navbar,
        graph_body
    ]
)

@dash_app1.callback(
    [Output("moisture-value", "children"),
     Output("timestamp", "children")],
    [Input("interval", "n_intervals")]
)
def update_latest(n):
    sql = "SELECT time, moisture FROM soil_moisture ORDER BY time DESC LIMIT 1;"
    df = pd.read_sql(sql, conn)

    if df.empty:
        return "데이터 없음", ""
    value = f"{df['moisture'].iloc[0]:.2f} %"
    timestamp = df['time'].iloc[0].strftime('%Y-%m-%d %H:%M:%S')
    return value, timestamp

@dash_app2.callback(
    Output("graph", "figure"),
    [Input("dropdown", "value"),
     Input("update-interval", "n_intervals"),
     Input("graph", "relayoutData")]
)
def get_graph(value, n, relayout_data):
    sql = """
        SELECT time, moisture FROM soil_moisture
        WHERE time > now() - interval '10 minutes'
        ORDER BY time ASC;
    """

    df = pd.read_sql(sql, conn)
    fig = go.Figure(data=go.Scatter(x=df['time'],
                                    y=df['moisture'],
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


if __name__ == "__main__":
    app.run(debug=True)