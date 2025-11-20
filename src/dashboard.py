# Plotly Dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc  # NYTT: Bootstrap komponenter

# Data och visualisering
import plotly.express as px
import plotly.graph_objects as go

# Matplotlib integration
import matplotlib
matplotlib.use('Agg')  # VIKTIGT: Sätter backend till icke-interaktiv för webbserver
import matplotlib.pyplot as plt
import io
import base64

# Egna moduler (behåll dessa som de är)
from .data_loader import load_and_anonymize_data
from .data_processor import OlympicAnalyzer
import os
import pandas as pd

# Initiera app med Bootstrap-tema (Välj t.ex. LUX, FLATLY, eller BOOTSTRAP)
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Olympic Games Analysis"

# --- DATA LOAD ---
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'athlete_events.csv')
df = load_and_anonymize_data(data_path)
analyzer = OlympicAnalyzer(df)

year_min = int(df['Year'].min())
year_max = int(df['Year'].max())
year_marks = {year: str(year) for year in range(year_min, year_max + 1, 8)}

# --- HJÄLPFUNKTIONER FÖR LAYOUT ---
def draw_section_header(title, desc):
    return dbc.Row([
        dbc.Col([
            html.H2(title, className="display-6"),
            html.P(desc, className="lead"),
            html.Hr(className="my-2")
        ])
    ], className="mb-4")

def draw_card(content, title=None, **card_kwargs):
    """Create a Bootstrap card with optional title and forward any card kwargs.

    Accepts arbitrary keyword arguments (e.g., className) so callers can customize
    the outer card element without changing this helper.
    """
    # default classes, allow overrides via card_kwargs
    defaults = {"className": "h-100 shadow-sm"}
    # Merge defaults with provided kwargs (kwargs override defaults)
    defaults.update(card_kwargs)
    return dbc.Card([
        dbc.CardHeader(title) if title else None,
        dbc.CardBody(content)
    ], **defaults)

# --- LAYOUT ---
app.layout = dbc.Container([
    
    # Huvudrubrik
    dbc.Row([
        dbc.Col(html.H1("Olympiska Spelen - Analys Dashboard", className="text-center my-5"), width=12)
    ]),

    # SEKTION 1: KANADA 3D (Behåll Plotly för interaktivitet)
    draw_section_header("Spotlight: Kanada i 3D", 
                        "Utforska idrottares fysiska profiler. Välj säsong och dra i tidsreglaget."),
    
    dbc.Row([
        # Kontrollpanel (Vänster)
        dbc.Col([
            draw_card([
                html.Label("Välj säsong", className="fw-bold"),
                dcc.RadioItems(
                    id='canada-season-filter',
                    options=[
                        {'label': ' Alla spel', 'value': 'All'},
                        {'label': ' Sommarspel', 'value': 'Summer'},
                        {'label': ' Vinterspel', 'value': 'Winter'}
                    ],
                    value='All',
                    labelStyle={'display': 'block', 'margin-bottom': '5px'}
                ),
                html.Hr(),
                html.Label("Filter", className="fw-bold"),
                dcc.RadioItems(
                    id='canada-medal-filter',
                    options=[
                        {'label': ' Alla deltagare', 'value': 'all'},
                        {'label': ' Endast medaljörer', 'value': 'medal'}
                    ],
                    value='medal',
                    labelStyle={'display': 'block', 'margin-bottom': '5px'}
                ),
                html.Hr(),
                html.Label("Tidsperiod"),
                dcc.RangeSlider(
                    id='canada-year-range',
                    min=year_min, max=year_max,
                    value=[max(1980, year_min), year_max], # Starta lite senare för prestanda
                    marks=None,
                    tooltip={'placement': 'bottom', 'always_visible': True}
                ),
                html.Small("X=Ålder, Y=Längd, Z=Vikt", className="text-muted mt-2")
            ], "Inställningar")
        ], width=12, lg=3, className="mb-3"),

        # Graf (Höger)
        dbc.Col([
            draw_card(dcc.Graph(id='canada-3d-profile', style={'height': '60vh'}), "3D Visualisering")
        ], width=12, lg=9, className="mb-3")
    ], className="mb-5"),

    # SEKTION 2: LAND-ANALYS & MATPLOTLIB
    draw_section_header("Uppgift 1 & Extra: Landstatistik & Matplotlib", 
                        "Statistik för specifika länder (Plotly) och statisk fördjupning (Matplotlib)."),

    dbc.Row([
        dbc.Col([
            html.Label("Välj land:", className="fw-bold"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': noc, 'value': noc} for noc in sorted(df['NOC'].unique())],
                value='CAN',
                clearable=False
            )
        ], width=12, md=6, className="mb-4")
    ]),

    # Plotly Grid
    dbc.Row([
        dbc.Col(draw_card(dcc.Graph(id='medals-by-sport')), width=12, md=6, className="mb-3"),
        dbc.Col(draw_card(dcc.Graph(id='medals-per-year')), width=12, md=6, className="mb-3"),
    ]),
    dbc.Row([
        dbc.Col(draw_card(dcc.Graph(id='age-histogram')), width=12, md=4, className="mb-3"),
        dbc.Col(draw_card(dcc.Graph(id='medal-types')), width=12, md=4, className="mb-3"),
        
        # --- HÄR ÄR MATPLOTLIB-GRAFEN ---
        dbc.Col(draw_card([
            html.H5("Matplotlib: Längd vs Vikt (Boxplot)", className="card-title"),
            # Här injicerar vi bilden
            html.Img(id='matplotlib-static-plot', style={'width': '100%', 'height': 'auto'})
        ]), width=12, md=4, className="mb-3"),
    ], className="mb-5"),

    # SEKTION 3: SPORT-ANALYS
    draw_section_header("Uppgift 2: Sportstatistik", "Detaljerad analys per sport."),
    
    dbc.Row([
        dbc.Col([
            html.Label("Välj sport:", className="fw-bold"),
            dcc.Dropdown(
                id='sport-dropdown',
                options=[{'label': s, 'value': s} for s in sorted(df['Sport'].unique())],
                value='Swimming',
                clearable=False
            )
        ], width=12, md=6, className="mb-4")
    ]),

    dbc.Row([
        dbc.Col(draw_card(dcc.Graph(id='sport-medals')), width=12, md=6, className="mb-3"),
        dbc.Col(draw_card(dcc.Graph(id='sport-ages')), width=12, md=6, className="mb-3"),
    ]),
    dbc.Row([
        dbc.Col(draw_card(dcc.Graph(id='sport-gender')), width=12, md=6, className="mb-3"),
        dbc.Col(draw_card(dcc.Graph(id='sport-medal-types')), width=12, md=6, className="mb-3"),
    ], className="mb-5"),

    # SEKTION 4: GLOBALT RACE
    draw_section_header("Global Medaljracet", "Animerad tidsresa."),
    
    dbc.Row([
        dbc.Col(draw_card([
            dbc.Row([
                dbc.Col([
                    html.Label("Säsong"),
                    dcc.RadioItems(
                        id='global-season-filter',
                        options=[{'label': 'Sommar', 'value': 'Summer'}, {'label': 'Vinter', 'value': 'Winter'}],
                        value='Summer',
                        inline=True,
                        inputStyle={"margin-left": "10px"}
                    )
                ], width=6),
                dbc.Col([
                    html.Label("Antal länder"),
                    dcc.Slider(id='global-top-n-slider', min=5, max=15, step=1, value=10)
                ], width=6)
            ])
        ], className="mb-3"), width=12)
    ]),
    
    dbc.Row([
        dbc.Col(draw_card(dcc.Graph(id='global-medal-race')), width=12)
    ], className="mb-5")

], fluid=True) # Fluid=True gör att containern fyller bredden snyggt


# --- CALLBACKS ---

# Ny callback för Matplotlib
@app.callback(
    Output('matplotlib-static-plot', 'src'),
    Input('country-dropdown', 'value')
)
def update_matplotlib_plot(country):
    """
    Genererar en statisk Matplotlib-figur och returnerar den som en bildsträng.
    Vi visualiserar fördelning av Vikt och Längd för det valda landet.
    """
    # Filtrera data
    country_df = df[df['NOC'] == country].dropna(subset=['Height', 'Weight'])
    
    if country_df.empty:
        return "" # Ingen bild om data saknas

    # 1. Skapa Matplotlib figuren
    fig, ax1 = plt.subplots(figsize=(6, 5))
    
    # Data to plot
    data_to_plot = [country_df['Height'], country_df['Weight']]
    
    # Skapa en boxplot
    parts = ax1.boxplot(data_to_plot, patch_artist=True, 
                        labels=['Längd (cm)', 'Vikt (kg)'])
    
    # Styling (Matplotlib style)
    colors = ['#2A9D8F', '#E9C46A']
    for patch, color in zip(parts['boxes'], colors):
        patch.set_facecolor(color)
    
    ax1.set_title(f'Fysisk fördelning: {country}')
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 2. Spara figuren till en buffer (i minnet)
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig) # Stäng figuren för att spara minne
    
    # 3. Konvertera till base64-sträng
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    return f"data:image/png;base64,{data}"


# --- BEFINTLIGA CALLBACKS (Oförändrade förutom inputs om namn ändrats) ---

@app.callback(
    [Output('medals-by-sport', 'figure'),
     Output('medals-per-year', 'figure'),
     Output('age-histogram', 'figure'),
     Output('medal-types', 'figure')],
    Input('country-dropdown', 'value')
)
def update_country_plots(country):
    # Top sports
    top_sports = analyzer.top_sports_by_medals(country)
    top_sports_df = top_sports.reset_index()
    top_sports_df.columns = ['Sport', 'Medals']
    fig1 = px.bar(top_sports_df, x='Medals', y='Sport', orientation='h',
                  title=f'Top Sporter: {country}', template='plotly_white')
    fig1.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=40, b=0))
    
    # Medals per Olympics
    medals_year = analyzer.medals_per_olympics(country)
    medals_year_df = medals_year.reset_index()
    medals_year_df.columns = ['Year', 'Medals']
    fig2 = px.line(medals_year_df, x='Year', y='Medals', markers=True,
                   title='Medaljutveckling', template='plotly_white')
    fig2.update_traces(line_color='#264653')
    fig2.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    
    # Age histogram
    ages = analyzer.age_distribution(country)
    fig3 = px.histogram(ages, nbins=20, title='Åldersfördelning', 
                        template='plotly_white', color_discrete_sequence=['#2A9D8F'])
    fig3.update_layout(showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
    
    # Medal types
    medal_stats = analyzer.get_medal_statistics(country)
    fig4 = px.pie(values=medal_stats.values, names=medal_stats.index, title='Medaljtyper',
                  color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})
    fig4.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    
    return fig1, fig2, fig3, fig4

@app.callback(
    [Output('sport-medals', 'figure'),
     Output('sport-ages', 'figure'),
     Output('sport-gender', 'figure'),
     Output('sport-medal-types', 'figure')],
    Input('sport-dropdown', 'value')
)
def update_sport_plots(sport):
    if not sport: return go.Figure(), go.Figure(), go.Figure(), go.Figure()
    
    analysis = analyzer.sport_analysis(sport)
    
    # Medal distribution
    mc = analysis['medal_countries'].head(10)
    fig1 = px.bar(x=mc.values, y=mc.index, orientation='h', title='Top 10 Länder', template='plotly_white')
    fig1.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(l=0, r=0, t=40, b=0))

    # Age
    fig2 = px.histogram(analysis['age_distribution'], nbins=20, title='Åldersfördelning',
                        color_discrete_sequence=['#E76F51'], template='plotly_white')
    fig2.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    # Gender
    gs = analysis['gender_split']
    fig3 = px.pie(values=gs.values, names=gs.index, title='Könsfördelning',
                  color_discrete_map={'M': '#4ECDC4', 'F': '#FF6B6B'})
    fig3.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    # Medal Types
    mt = analysis['medal_types']
    fig4 = px.pie(values=mt.values, names=mt.index, title='Medaljtyper',
                  color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'})
    fig4.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    
    return fig1, fig2, fig3, fig4

@app.callback(
    Output('canada-3d-profile', 'figure'),
    [Input('canada-season-filter', 'value'), Input('canada-medal-filter', 'value'), Input('canada-year-range', 'value')]
)
def update_canada_3d(season, medal_filter, year_range):
    medal_only = medal_filter == 'medal'
    # NOTERA: Här antar jag att analyzer-funktionen finns. Om inte, hantera felet.
    try:
        profile_df = analyzer.country_athlete_profile('CAN', season=season, medal_only=medal_only)
    except Exception:
        # Fallback om metoden inte finns exakt som anropat
        return go.Figure()

    if year_range:
        profile_df = profile_df[(profile_df['Year'] >= year_range[0]) & (profile_df['Year'] <= year_range[1])]

    if profile_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Ingen data", showarrow=False)
        return fig

    size_map = {'Gold': 15, 'Silver': 12, 'Bronze': 10, 'Ingen medalj': 6}
    medal_disp = profile_df['Medal'].fillna('Ingen medalj')
    profile_df['Size'] = medal_disp.map(size_map).fillna(5)
    
    color_map = {'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32', 'Ingen medalj': '#264653'}
    
    fig = px.scatter_3d(
        profile_df, x='Age', y='Height', z='Weight',
        color=medal_disp, size='Size', hover_name='Event',
        color_discrete_map=color_map,
        title="Kanadensiska Atleter (3D)",
        animation_frame='Year'
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1)))
    return fig

@app.callback(
    Output('global-medal-race', 'figure'),
    [Input('global-season-filter', 'value'), Input('global-top-n-slider', 'value')]
)
def update_global_race(season, top_n):
    try:
        data = analyzer.global_medal_race(season=season, top_n=top_n)
    except:
        return go.Figure()
        
    if data.empty: return go.Figure()

    fig = px.bar(data, x='Medals', y='NOC', color='NOC', animation_frame='Year', 
                 orientation='h', title="Medaljtoppen över tid")
    fig.update_layout(xaxis_title="", yaxis_title="", showlegend=False,
                      margin=dict(l=0, r=0, t=40, b=0))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)