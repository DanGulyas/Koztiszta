import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Mock data for "Rendelések"
rekord_data = {
    'Termék cikkszáma': ['152000177', '152000178', '152000179', '152000180'],
    'Total': [33203, 605, 1, 2739]
}

ure_data = {
    'Céllétesítmények száma': ['Nem üres', 'Üres'],
    'Total': [42073, 6385]
}

status_data = {
    'Megrendelés státusza': ['Van', 'Nincs'],
    'Rendelésszám': [36542, 6]
}

ten_days_data = {
    'Üres Mérés': [0],
    'Nem üres': [36398]
}

rendeleshez_egy_meres_data = [2179]
rendeleshez_egy_meres_data_dict = {'Egy rendeléshez több mérés van': ['Igen', 'Nem'],
    'Mérés': [28452, 2179]}

kpi_lista = {'Más cikkszámokon mérlegjegy': 1,
             'Üres Céllétesítmény rekordok': 6385,
             'Teljesült mérések mérési adat nélkül': 6,
             'Rendeléshez több, mint 1 mérés van': 2179,
             '10 napja letelt rendeléseken nincs mérés': 0}

#                                                               SZERZODESEK SZERZLDESTETELEK

tiz_nap_vazlat = {
    "10 napnál régebbi, Vázlat státuszú szerződések?": ["Nem", "Nincs aktiválási dátum"],
        "Count": [2126, 86],
    }

tiz_nap_modositas = {
    "10 napnál régebbi, Módosítás szükséges státuszú szerződések?": ["Igen", "Nem", "Nincs aktiválási dátum"],
    "Count": [294, 1832, 86]
}

szerztetel_SAP_azonosito = {
    "Szerződéstételen van SAP azonosító?": ["Igen", "Nem"],
        "Count": [1458, 754]
    }

szerztetel_szolgcikk = {
    "Szerződéstételen rajta van a kapcsolódó szolg. cikk?": ["Igen", "Nem"],
        "Count": [2212, 0],
    }

kpi_lista_szerzodesek = {'10 napnál régebbi, vázlat státuszú szerződések': 0,
             '10 napnál régebbi, Módosítás szükséges státuszú szerződések': 294,
             'Szerződéstételen nincs SAP azonosító': 754,
             'Szerződéstételen nincs kapcsolódó szolg. cikk': 0,
             'SAP-SF között szerződéstételen lévő számlázási tétel nem egyezik meg': 0,
             'SAP-SF között szerződéstételek státusza nem egyezik meg': 53,
             'SAP szerződéstétel és cikk árazása nem egyezik meg': 40,}

celletesitmenyszerz_data = {
    "Céllétesítmények száma": ["Nem Üres", "Üres"],
    "Count": [42581, 6455]
}

SAP_SF_szamltetel = [0]               # Nincs találat = 1022   SAP-SF között szerződéstételek státusza egyezik e

SAP_SF_szerztetelstatusz = {
"SAP-SF között szerződéstételek száma egyezik -e?": ["Igen", "Nem"],
"Count":[1405,	53]}


SAP_SF_szerztetelszolgcikk  = [0]               # Nincs találat = 1022

SAP_SF_arazas = [40]

#                                       Convert rendeles dictionaries to DataFrames
df_rekord = pd.DataFrame(rekord_data)
df_ure = pd.DataFrame(ure_data)
df_status = pd.DataFrame(status_data)
df_ten_days = pd.DataFrame(ten_days_data)
df_egy_rendeles = pd.DataFrame(rendeleshez_egy_meres_data)
df_egy_rendeles_dict = pd.DataFrame(rendeleshez_egy_meres_data_dict)
df_kpi = pd.DataFrame(list(kpi_lista.items()), columns=['KPI', 'Hibák száma'])
# Convert rendeles dictionaries to DataFrames
df_tiz_nap_vazlat = pd.DataFrame(tiz_nap_vazlat)
df_tiz_nap_modositas = pd.DataFrame(tiz_nap_modositas)
df_szerztetel_SAP_azonosito = pd.DataFrame(szerztetel_SAP_azonosito)
df_szerztetel_szolgcikk = pd.DataFrame(szerztetel_szolgcikk)
df_kpi2 = pd.DataFrame(list(kpi_lista_szerzodesek.items()), columns=['KPI', 'Hibák száma'])
df_celletesitmenyszerz = pd.DataFrame(celletesitmenyszerz_data)
df_SAP_SF_szamltetel = pd.DataFrame(SAP_SF_szamltetel)
df_SAP_SF_szerztetelstatusz = pd.DataFrame(SAP_SF_szerztetelstatusz).rename(columns=str.strip)
df_SAP_SF_szerztetelszolgcikk = pd.DataFrame(SAP_SF_szerztetelszolgcikk)
df_SAP_SF_arazas = pd.DataFrame(SAP_SF_arazas)



# Lying stacked bar chart with total values displayed
lying_bar_fig = go.Figure()
# Adding bars to the lying bar chart with stacking enabled
for index, row in df_rekord.iterrows():
    lying_bar_fig.add_trace(go.Bar(
        y=[row['Termék cikkszáma']],
        x=[row['Total']],
        orientation='h',
        name=row['Termék cikkszáma'],
        text=str(row['Total']),
        hoverinfo='text',
        marker=dict(color=px.colors.qualitative.Set2[index], line=dict(color='black', width=2))
    ))

lying_bar_fig.update_layout(
    title="Hány olyan mérés van, amin nem a megfelelő cikkszám szerepel?",   # text box kellene majd csak
    xaxis_title="Esetszám",
    yaxis_title="Termék cikkszáma",
    plot_bgcolor="#1e1e1e",
    paper_bgcolor="#1e1e1e",
    font=dict(color="white"),
    barmode="stack",  # Ensures that the bars are stacked
    showlegend=True,  # Show the legend
    legend=dict(x=1, y=1)  # Position legend on the right side
)

# Add text with shadow behind bars
for trace in lying_bar_fig.data:
    trace.update(textposition='inside', texttemplate='%{text}', insidetextfont=dict(color='white', size=12))

# Create Treemap for "ure_data"
ure_data_fig = px.treemap(df_ure,
                          path=['Céllétesítmények száma'],
                          # This is the column you want to use as hierarchical categories
                          values='Total',  # Values to represent the size of each block
                          title='Hiányos céllétesítmény nevek száma',
                          template='plotly_dark')

# Ensure proper text formatting
for trace in ure_data_fig.data:
    trace.update(
        texttemplate='%{label}: %{value}',  # Label and value to show inside each block
        textposition='middle center',  # A valid textposition for treemaps
        insidetextfont=dict(color='white', size=12)
    )

# Update layout to make sure it's clear
ure_data_fig.update_layout(
    plot_bgcolor="#1e1e1e",
    paper_bgcolor="#1e1e1e",
    font=dict(color="white"),
    showlegend=True  # Show the legend if needed
)

# Bar chart for "status_data"
status_data_fig = px.bar(df_status, x='Megrendelés státusza', y='Rendelésszám',
                         title='Minden megrendelésre van e mérés', template='plotly_dark')    #aktív?
for trace in status_data_fig.data:
    trace.update(textposition='outside', texttemplate='%{y}', insidetextfont=dict(color='black', size=12))
status_data_fig.update_layout(
    yaxis=dict(
        tickmode="array",
        automargin=True,
        range=[0, df_status['Rendelésszám'].max() * 1.2]),
    xaxis=dict(
        title='',  # Remove the x-axis title
    ),
    margin=dict(t=50, b=40),  # Adjust top and bottom margin
    title_x=0.5
)

# KPI count for empty "Céllétesítmények száma"
empty_count = df_ure['Total'].sum()

# Extract "Üres Mérés" value
empty_measure = df_ten_days['Üres Mérés'][0]
empty_measure_display = f"{empty_measure} ✅" if empty_measure == 0 else str(empty_measure)

# Egy rendeleshez egy meres
rendeles_kpi = df_egy_rendeles.iloc[0, 0]  # Select the first row, first column as a scalar
rendeles_kpi_display = f"{rendeles_kpi} ✅" if rendeles_kpi == 0 else str(rendeles_kpi)

rendeles_kpi_dict_fig = px.bar(df_egy_rendeles_dict, x='Egy rendeléshez több mérés van', y='Mérés',
                         title='Minden megrendelésre egy mérés van e?', template='plotly_dark')
for trace in rendeles_kpi_dict_fig.data:
    trace.update(textposition='outside', texttemplate='%{y}', insidetextfont=dict(color='white', size=12))
rendeles_kpi_dict_fig.update_layout(
    yaxis=dict(
        tickmode="array",
        automargin=True,
        range=[0, df_egy_rendeles_dict['Mérés'].max() * 1.2]),
        xaxis=dict(
        title=''  # Hides x-axis labels
    ),
    margin=dict(t=50, b=40),  # Adjust top and bottom margin
    title_x=0.5  # Center the title
)


# Generate treemap for "10 napnál régebbi, Vázlat státuszú szerződés?"
fig_vazlat = px.bar(df_tiz_nap_vazlat,
                    x="Count",
                    y="10 napnál régebbi, Vázlat státuszú szerződések?",
                    orientation='h',  # Set to 'v' if you want vertical bars
                    title="10 napnál régebbi, Vázlat státuszú szerződések")
for trace in fig_vazlat.data:
    trace.update(textposition='inside', texttemplate='%{x}', insidetextfont=dict(color='white', size=12))
    fig_vazlat.update_layout(
        yaxis=dict(
            tickmode="array",
            automargin=True  # Ensures labels fit inside the figure
        ),
        xaxis=dict(
            title='',  # Remove the x-axis title
        ),
        xaxis_title="",  # Label for X-axis
        yaxis_title="",  # Remove redundant y-axis title if needed
        title_x=0.5  # Center the title
    )



# Generate Treemap for "Módosítás szükséges státuszú szerződés?"
fig_modositas = px.bar(df_tiz_nap_modositas,
                           y="10 napnál régebbi, Módosítás szükséges státuszú szerződések?",
                           x="Count",
                           orientation='h',  # Set to 'v' if you want vertical bars
                           title="10 napnál régebbi, Módosítás szükséges státuszú szerződések")
for trace in fig_modositas.data:
    trace.update(textposition='inside', texttemplate='%{x}', insidetextfont=dict(color='white', size=12))
fig_modositas.update_layout(
        yaxis=dict(
            tickmode="array",
            automargin=True  # Ensures labels fit inside the figure
        ),
        xaxis_title="",  # Label for X-axis
        yaxis_title="",  # Remove redundant y-axis title if needed
        title_x=0.5  # Center the title
    )

# Generate Stacked Bar Chart for "Szerződéstételen van SAP azonosító?"
fig_sap_azonosito = go.Figure()
fig_sap_azonosito.add_trace(go.Bar(
    x=df_szerztetel_SAP_azonosito['Count'],  # x represents the count values
    y=df_szerztetel_SAP_azonosito['Szerződéstételen van SAP azonosító?'],  # y represents the categories
    orientation='h',  # Horizontal bars
    name="SAP Azonosító",
    text=df_szerztetel_SAP_azonosito['Count'],  # Display the count as text
    textposition='inside'  # Place the text inside the bars
))
fig_sap_azonosito.update_layout(
    title="Szerződéstételen van e SAP azonosító?",  # Title for the chart
    barmode='stack'  # Stack the bars if needed (for multiple categories)
)

# Generate Lying Stacked Bar Chart for "Mennyiség / Szerződéstételen rajta van az értékesített szolg. cikk?"
fig_szolgcikk = go.Figure()

fig_SF_SAP_szerztetelstatusz = px.treemap(
    df_SAP_SF_szerztetelstatusz,
    path=["SAP-SF között szerződéstételek száma egyezik -e?"],  # Ensure this matches the cleaned name
    values="Count",
    title="SAP-SF között szerződéstételek száma egyezik -e?"
)


empty_measure_szolgcikk = df_szerztetel_szolgcikk['Count'][1]
empty_measure_szolgcikk_display = f"{empty_measure_szolgcikk} ✅" if empty_measure_szolgcikk == 0 else str(empty_measure_szolgcikk)

empty_measure_SAP_SF_szamltetel = df_SAP_SF_szamltetel.iloc[0, 0]
empty_measure_SAP_SF_szamltetel_display = f"{empty_measure_SAP_SF_szamltetel} ✅" if empty_measure_SAP_SF_szamltetel == 0 else str(empty_measure_SAP_SF_szamltetel)

empty_measure_SAP_SF_szerztetelszolgcikk = df_SAP_SF_szerztetelszolgcikk.iloc[0, 0]
empty_measure_SAP_SF_szerztetelszolgcikk_display = f"{empty_measure_SAP_SF_szerztetelszolgcikk} ✅" if empty_measure_SAP_SF_szerztetelszolgcikk == 0 else str(empty_measure_SAP_SF_szerztetelszolgcikk)

empty_measure_SF_SAP_arazas = df_SAP_SF_arazas.iloc[0, 0]
empty_measure_SF_SAP_arazas_display = f"{empty_measure_SF_SAP_arazas} ✅" if empty_measure_SF_SAP_arazas == 0 else str(empty_measure_SF_SAP_arazas)




# Create the bar chart
bar_chart = go.Bar(
    x=list(kpi_lista_szerzodesek.keys()),
    y=list(kpi_lista_szerzodesek.values()),
    marker=dict(color='#1f77b4')
)

# Create the pie chart
pie_chart = go.Pie(
    labels=list(kpi_lista_szerzodesek.keys()),
    values=list(kpi_lista_szerzodesek.values()),
    hole=0.3,
    textinfo='none',          # Hide text inside the pie
    hoverinfo='none',
    marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
)


celletesitmenyszerz_data_fig = px.treemap(df_ure,
                          path=['Céllétesítmények száma'],
                          values='Total',  # Values to represent the size of each block
                          title='Hiányos céllétesítmény nevek száma',
                          template='plotly_dark')



# External dark theme stylesheet
external_stylesheets = ['https://cdn.jsdelivr.net/npm/bootswatch@5.3.0/dist/darkly/bootstrap.min.css']

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
app.title = "Köztiszta rendelések, szerződések, szerződéstételek DQ"

# Dashboard layout
app.layout = html.Div([  # Start of the layout
    html.H1("Köztiszta szerződések, szerződéstételek, rendelések adatminőség dashboard SF-SAP", style={
        "textAlign": "center",
        "backgroundColor": "#1e1e1e",
        "color": "white",
        "padding": "10px",
        "borderRadius": "10px",
    }),

    dcc.Tabs([
        dcc.Tab(
            label="Szerződések, szerződéstételek",
            children=[
                html.Div([
                    html.Div([
                        html.H2("Fő KPI-ok összegzése", style={
                            "textAlign": "center", "color": "white",
                            "padding": "20px", "fontSize": "20px"
                        }),
                        html.Div([
                            dcc.Graph(
                                id="kpi-bar-chart2",
                                figure=px.bar(
                                    df_kpi2, x='KPI', y='Hibák száma',
                                    template="plotly_dark"
                                ).update_layout(
                                    plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e",
                                    font=dict(color="white"), legend=dict(x=1, y=1),
                                    xaxis=dict(
                                        title='',  # Remove the x-axis title
                                    ),
                                ).update_traces(
                                    texttemplate='%{y}', textposition='inside',
                                    insidetextfont=dict(color='white', size=12)
                                ),
                            ),
                            dcc.Graph(
                                id="kpi-pie-chart2",
                                figure=px.pie(
                                    df_kpi2, values='Hibák száma', names='KPI',
                                    hole=0.4, template="plotly_dark"
                                ).update_traces(
                                    textinfo='none',
                                ).update_layout(
                                    plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e",
                                    font=dict(color="white"), legend=dict(x=1, y=1),
                                )
                            )
                        ], style={
                            "display": "flex", "justifyContent": "space-between",
                            "flexDirection": "row", "padding": "10px"
                        })
                    ], style={
                        "display": "flex", "flexDirection": "column", "alignItems": "center"
                    }),
                ]),

                html.Div([
                    dcc.Graph(figure=fig_vazlat.update_layout(
                        plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e",
                        font=dict(color="white"), legend=dict(x=1, y=1)
                    )),
                    dcc.Graph(figure=fig_modositas.update_layout(
                        plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e",
                        font=dict(color="white"), legend=dict(x=1, y=1)
                    )),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'}),

                html.Div([
                    dcc.Graph(figure=fig_sap_azonosito.update_layout(
                        plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e",
                        font=dict(color="white"), legend=dict(x=1, y=1)
                    )),
                    dcc.Graph(figure=fig_SF_SAP_szerztetelstatusz.update_layout(
                        plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e",
                        font=dict(color="white"), legend=dict(x=1, y=1)
                    )),
                    html.H3("Hány szerződéstételen nincs rajta a kapcsolódó szolgáltatási cikk?",
                            style={"textAlign": "center", "color": "#ffcc00"}),
                    html.H1(empty_measure_szolgcikk_display,
                            style={"textAlign": "center", "color": "#00ff00", "fontWeight": "bold",
                                   "fontSize": "50px"}),

                    html.H3("SF és SAP között hány szerződéstételen különbözik a számlázási mód?",
                            style={"textAlign": "center", "color": "#ffcc00"}),
                    html.H1(empty_measure_SAP_SF_szamltetel_display,
                            style={"textAlign": "center", "color": "#00ff00", "fontWeight": "bold",
                                   "fontSize": "50px"}),

                    html.H3("SF és SAP között hány szerződéstételen nem egyeznek meg a szolgáltatás cikkek?",
                            style={"textAlign": "center", "color": "#ffcc00"}),
                    html.H1(empty_measure_SAP_SF_szerztetelszolgcikk_display,
                            style={"textAlign": "center", "color": "#00ff00", "fontWeight": "bold",
                                   "fontSize": "50px"}),
                    html.H3("SAP oldalon hány szerződéstételnek az árazása nem egyezik a szolgáltatási cikk árazásával?",
                            style={"textAlign": "center", "color": "#ffcc00"}),
                    html.H1(empty_measure_SF_SAP_arazas_display,
                            style={"textAlign": "center", "color": "#ff0000", "fontWeight": "bold",
                                   "fontSize": "50px"}),

                ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center',
                          "color": "white", "backgroundColor": "#1e1e1e"}),

            ],
            style={"backgroundColor": "#1e1e1e", "color": "white"},
            selected_style={"backgroundColor": "white", "color": "black", "fontWeight": "bold"}
        ),

        dcc.Tab(
            label="Rendelések",
            children=[
                html.Div([
                    html.Div([
                        html.H2("Fő KPI-ok összegzése", style={
                            "textAlign": "center", "color": "white",
                            "padding": "20px", "fontSize": "20px"
                        }),
                        html.Div([
                            dcc.Graph(
                                id="kpi-bar-chart",
                                figure=px.bar(
                                    df_kpi, x='KPI', y='Hibák száma',
                                    template="plotly_dark"
                                ).update_layout(
                                    plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e",
                                    font=dict(color="white"), legend=dict(x=1, y=1),
                                    xaxis=dict(
                                        title='',  # Remove the x-axis title
                                    ),
                                ).update_traces(
                                    texttemplate='%{y}', textposition='inside',
                                    insidetextfont=dict(color='white', size=12)
                                )
                            ),
                            dcc.Graph(
                                id="kpi-pie-chart",
                                figure=px.pie(
                                    df_kpi, values='Hibák száma', names='KPI',
                                    hole=0.4, template="plotly_dark"
                                ).update_traces(
                                    textinfo='none',
                                ).update_layout(
                                    plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e",
                                    font=dict(color="white"), legend=dict(x=1, y=1)
                                )
                            )
                        ], style={
                            "display": "flex", "justifyContent": "space-between",
                            "flexDirection": "row", "padding": "10px"
                        })
                    ], style={"display": "flex", "flexDirection": "column", "alignItems": "center"}),

                    dcc.Graph(id="lying-bar-chart", figure=lying_bar_fig),
                    dcc.Graph(id="ure-bar-chart", figure=ure_data_fig),
                    dcc.Graph(id="status-bar-chart", figure=status_data_fig),
                    dcc.Graph(id="rendeles-bar-chart", figure=rendeles_kpi_dict_fig),


                    html.Div([
                        html.H3("Rendelések száma, ahol a szállítás napja már 10 napja letelt, de nincs rá mérés",
                                style={"textAlign": "center", "color": "#ffcc00"}),
                        html.H1(empty_measure_display,
                                style={"textAlign": "center", "color": "#00ff00", "fontWeight": "bold",
                                       "fontSize": "50px"}),
                    ])
                ])
            ],
            style={"backgroundColor": "#1e1e1e", "color": "white"},
            selected_style={"backgroundColor": "white", "color": "black", "fontWeight": "bold"}
        )
        ])
        ])

server = app.server

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)

