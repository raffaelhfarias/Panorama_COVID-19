from dash import Dash, html, dcc, Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import dash

import pandas as pd
import numpy as nd
import json


CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# =====================================================================
# Data Load
df = pd.read_csv('df.csv')
df_world = pd.read_csv('df_world.csv')

geo_json = json.load(open("geojson/countries_geo.json", "r"))

select_columns = {#"location ": "Total Mundial",
                "total_cases": "Casos Acumulados", 
                "new_cases": "Novos Casos", 
                "total_deaths": "Óbitos Totais",
                "new_deaths": "Novos Óbitos por dia"}


# =====================================================================
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

fig = px.choropleth_mapbox(df, locations="iso_code",
    geojson=geo_json, zoom=4, color="total_cases", color_continuous_scale="orrd", opacity=0.4,
    hover_data={"total_cases": True, "new_cases": True, "new_deaths": True, "location": True}
    )

fig.update_layout(
                # mapbox_accesstoken=token,
                paper_bgcolor="#242424",
                mapbox_style="carto-darkmatter",
                autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=False,)

df_brasil = df[df["location"] == "Brazil"]

fig2 = go.Figure(layout={"template":"plotly_dark"})
fig2.add_trace(go.Scatter(x=df_brasil["location"], y=df_brasil["total_cases"]))
fig2.update_layout(
    paper_bgcolor="#242424",
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    )

app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col([
                    html.Div([
                        html.Img(id="logo", src=app.get_asset_url("rhfariasn.png"), height=70),
                        html.H5(children="Evolução COVID-19"),
                        dbc.Button("BRA", color="primary", id="location-button", size="lg")
                    ], style={"background-color": "#1E1E1E", "margin": "-25px", "padding": "25px"}),
                    html.P("Informe a data na qual deseja obter informações:", style={"margin-top": "40px"}),
                    html.Div(
                            className="div-for-dropdown",
                            id="div-test",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=df.groupby("continent")["date"].min().max(),
                                    max_date_allowed=df.groupby("continent")["date"].max().min(),
                                    initial_visible_month=df.groupby("continent")["date"].min().max(),
                                    date=df.groupby("continent")["date"].max().min(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),

                    dbc.Row([
                        #dbc.Col([dbc.Card([   
                                #dbc.CardBody([
                                    #html.Span("Casos totais mundial", className="card-text"),
                                    #html.H3(style={"color": "#adfc92"}, id="casos-totais-text"),
                                    #html.Span("Casos totais mundial na data", className="card-text"),
                                    #html.H5(id="casos-totais-nadata-text"),
                                    #])
                                #], color="light", outline=True, style={"margin-top": "10px",
                                       #"box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        #"color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Casos confirmados totais", className="card-text"),
                                    html.H3(style={"color": "#389fd6"}, id="casos-confirmados-text"),
                                    html.Span("Novos casos na data", className="card-text"),
                                    html.H5(id="novos-casos-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Óbitos confirmados", className="card-text"),
                                    html.H3(style={"color": "#DF2935"}, id="obitos-text"),
                                    html.Span("Óbitos na data", className="card-text"),
                                    html.H5(id="obitos-na-data-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF"})], md=4),
                    ]),

                    html.Div([
                        html.P("Selecione que tipo de dado deseja visualizar:", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                                        id="location-dropdown",
                                        options=[{"label": j, "value": i}
                                            for i, j in select_columns.items()
                                        ],
                                        value="new_cases",
                                        style={"margin-top": "10px"}
                                    ),
                        dcc.Graph(id="line-graph", figure=fig2, style={
                            "background-color": "#242424",
                            }),
                        ], id="teste")
                ], md=5, style={
                          "padding": "25px",
                          "background-color": "#242424"
                          }), 

            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[dcc.Graph(id="choropleth-map", figure=fig, 
                            style={'height': '100vh', 'margin-right': '10px'})],
                    ),
                ], md=7),
            ],)
    ], fluid=True, 
)

# =====================================================================
# Interatividade

@app.callback(
    [
        #Output("casos-totais-text", "children"),
        #Output("casos-totais-nadata-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children"),
    ], [Input("date-picker", "date"), Input("location-button", "children")]
)
def display_status(date, location):
    # print(location, date)
    if location == "BRA":
        df_data_on_date = df_brasil[df_brasil["date"] == date]
    else:
        df_data_on_date = df[(df["iso_code"] == location) & (df["date"] == date)]

    #casos_totais = "-" if df_data_on_date["total_cases"].isna().values[0]  else f'{int(df_data_on_date["total_cases"].values[0]):,}'.replace(",", ".")
    #casos_totais_nadata = "-" if df_data_on_date["total_cases"].isna().values[0]  else f'{int(df_data_on_date["total_cases"].values[0]):,}'.replace(",", ".") 
    casos_acumulados = "-" if df_data_on_date["total_cases"].isna().values[0]  else f'{int(df_data_on_date["total_cases"].values[0]):,}'.replace(",", ".") 
    casos_novos = "-" if df_data_on_date["new_cases"].isna().values[0]  else f'{int(df_data_on_date["new_cases"].values[0]):,}'.replace(",", ".") 
    obitos_acumulado = "-" if df_data_on_date["total_deaths"].isna().values[0]  else f'{int(df_data_on_date["total_deaths"].values[0]):,}'.replace(",", ".") 
    obitos_novos = "-" if df_data_on_date["new_deaths"].isna().values[0]  else f'{int(df_data_on_date["new_deaths"].values[0]):,}'.replace(",", ".") 
    return (
            #casos_totais, 
            #casos_totais_nadata, 
            casos_acumulados, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos,
            )

@app.callback(
        Output("line-graph", "figure"),
        [Input("location-dropdown", "value"), Input("location-button", "children")]
)
def plot_line_graph(plot_type, location):
    if location == "BRA":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df[(df["iso_code"] == location)]
    fig2 = go.Figure(layout={"template":"plotly_dark"})
    bar_plots = ["new_cases", "new_deaths"]

    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["date"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["date"], y=df_data_on_location[plot_type]))
    
    fig2.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return fig2

@app.callback(
    Output("choropleth-map", "figure"), 
    [Input("date-picker", "date")]
)
def update_map(date):
    df_data_on_states = df[df["date"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="iso_code", geojson=geo_json, 
        center={"lat": CENTER_LAT, "lon": CENTER_LON}, #https://www.google.com/maps/ -> right click -> get lat/lon
        zoom=4, color="total_cases", color_continuous_scale="orrd", opacity=0.55,
        hover_data={"total_cases": True, "new_cases": True, "new_deaths": True, "location": True}
        )

    fig.update_layout(paper_bgcolor="#242424", mapbox_style="carto-darkmatter", autosize=True,
                    margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig  

@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    
    else:
        return "BRA"

if __name__ == "__main__":
	app.run_server(debug=True, port='8084')
