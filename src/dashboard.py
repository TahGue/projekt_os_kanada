# Plotly Dash for interactive web dashboards
# Documentation: https://dash.plotly.com/
# Version: 2.14.2
from dash import Dash, html, dcc, Input, Output

# Plotly Express for data visualization
# Documentation: https://plotly.com/python/plotly-express/
# Version: 5.17.0
import plotly.express as px
import plotly.graph_objects as go

from .data_loader import load_and_anonymize_data
from .data_processor import OlympicAnalyzer
import os

# Skapa app med enhetlig design
app = Dash(__name__, external_stylesheets=['/assets/style.css'])
app.title = "Olympic Games Analysis"

# Ladda data
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'athlete_events.csv')
df = load_and_anonymize_data(data_path)
analyzer = OlympicAnalyzer(df)

year_min = int(df['Year'].min())
year_max = int(df['Year'].max())
year_marks = {year: str(year) for year in range(year_min, year_max + 1, 8)}

# Layout - användarvänlig och enhetlig design
app.layout = html.Div([
    html.H1("Olympiska Spelen - Analys Dashboard", className='header'),

    # KANADA-SPOTLIGHT SEKTION
    html.Div([
        html.Div([
            html.H2("Spotlight: Kanada i 3D"),
            html.P(
                "Utforska kanadensiska idrottares fysiska profiler. Välj säsong, filtrera på medaljörer och dra i tidsreglaget för att se hur atleternas ålder, längd och vikt förändras över åren.",
                className='section-description'
            )
        ], className='section-header'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("Välj säsong"),
                        dcc.RadioItems(
                            id='canada-season-filter',
                            options=[
                                {'label': 'Alla spel', 'value': 'All'},
                                {'label': 'Sommarspel', 'value': 'Summer'},
                                {'label': 'Vinterspel', 'value': 'Winter'}
                            ],
                            value='All',
                            className='radio-group'
                        )
                    ], className='control-card'),
                    html.Div([
                        html.Label("Vilka idrottare ska visas?"),
                        dcc.RadioItems(
                            id='canada-medal-filter',
                            options=[
                                {'label': 'Alla deltagare', 'value': 'all'},
                                {'label': 'Endast medaljörer', 'value': 'medal'}
                            ],
                            value='medal',
                            className='radio-group'
                        )
                    ], className='control-card')
                ], className='control-panel'),
                html.Div([
                    html.Label("Tidsperiod"),
                    dcc.RangeSlider(
                        id='canada-year-range',
                        min=year_min,
                        max=year_max,
                        value=[max(1920, year_min), year_max],
                        allowCross=False,
                        marks=year_marks,
                        tooltip={'placement': 'bottom', 'always_visible': False}
                    )
                ], className='slider-card'),
                html.P(
                    "Axlar: X visar ålder (år), Y visar längd (cm) och Z visar vikt (kg). Animeringen bläddrar år för år – tryck play för att följa utvecklingen.",
                    className='axis-note'
                )
            ], className='section-column section-column--info'),
            html.Div([
                html.Div(dcc.Graph(id='canada-3d-profile'), className='graph-card')
            ], className='section-column section-column--visual')
        ], className='section-content section-content--split')
    ], className='section highlight-section'),
    
    # LAND-ANALYS SEKTION
    html.Div([
        html.Div([
            html.H2("Uppgift 1: Landstatistik"),
            html.P(
                "Visualisera medaljfördelning och utveckling för det valda landet.",
                className='section-description'
            )
        ], className='section-header'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': noc, 'value': noc} for noc in sorted(df['NOC'].unique())],
            value='CAN',  # Kanada
            className='dropdown'
        ),
        html.P(
            "Axlarna anger medaljranken per sport, antal medaljer per spel, åldersfördelningen samt medaljtypernas proportioner för det valda landet.",
            className='axis-note'
        ),
        html.Div([
            html.Div(dcc.Graph(id='medals-by-sport'), className='graph-card'),
            html.Div(dcc.Graph(id='medals-per-year'), className='graph-card'),
            html.Div(dcc.Graph(id='age-histogram'), className='graph-card'),
            html.Div(dcc.Graph(id='medal-types'), className='graph-card')
        ], className='graph-grid')
    ], className='section'),
    
    # SPORT-ANALYS SEKTION
    html.Div([
        html.Div([
            html.H2("Uppgift 2: Sportstatistik"),
            html.P(
                "Följ medaljer, åldrar och könsfördelning inom vald sport.",
                className='section-description'
            )
        ], className='section-header'),
        dcc.Dropdown(
            id='sport-dropdown',
            options=[{'label': sport, 'value': sport} for sport in sorted(df['Sport'].unique())],
            value='Swimming',
            className='dropdown'
        ),
        html.P(
            "Axlarna beskriver medaljer per land (x = medaljer, y = land), åldersfördelning (x = ålder i år, y = antal idrottare), könsfördelning samt medaljtyper inom vald sport.",
            className='axis-note'
        ),
        html.Div([
            html.Div(dcc.Graph(id='sport-medals'), className='graph-card'),
            html.Div(dcc.Graph(id='sport-ages'), className='graph-card'),
            html.Div(dcc.Graph(id='sport-gender'), className='graph-card'),
            html.Div(dcc.Graph(id='sport-medal-types'), className='graph-card')
        ], className='graph-grid')
    ], className='section'),

    # GLOBAL ANIMERING SEKTION
    html.Div([
        html.Div([
            html.H2("Global Medaljracet – Animerad översikt"),
            html.P(
                "Se hur världens främsta nationslag tävlar om medaljer över tid. Animeringen uppdateras år för år – tryck play för att starta racet.",
                className='section-description'
            )
        ], className='section-header'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Label("Säsong"),
                        dcc.RadioItems(
                            id='global-season-filter',
                            options=[
                                {'label': 'Alla spel', 'value': 'All'},
                                {'label': 'Sommarspel', 'value': 'Summer'},
                                {'label': 'Vinterspel', 'value': 'Winter'}
                            ],
                            value='Summer',
                            className='radio-group'
                        )
                    ], className='control-card'),
                    html.Div([
                        html.Label("Visa topp NOC per år"),
                        dcc.Slider(
                            id='global-top-n-slider',
                            min=5,
                            max=15,
                            step=1,
                            value=8,
                            marks={i: str(i) for i in range(5, 16, 2)}
                        )
                    ], className='control-card')
                ], className='control-panel'),
                html.P(
                    "Axlar: Y listar NOC-koder (länder) och X visar antal medaljer det året. Play-knappen låter dig följa utvecklingen över alla spel.",
                    className='axis-note'
                )
            ], className='section-column section-column--info'),
            html.Div([
                html.Div(dcc.Graph(id='global-medal-race'), className='graph-card')
            ], className='section-column section-column--visual')
        ], className='section-content section-content--split')
    ], className='section')
    
], className='container')


# CALLBACKS - Interaktivitet
# Dash callback pattern for interactive updates
# Reference: Plotly Dash documentation - https://dash.plotly.com/basic-callbacks

@app.callback(
    [Output('medals-by-sport', 'figure'),
     Output('medals-per-year', 'figure'),
     Output('age-histogram', 'figure'),
     Output('medal-types', 'figure')],
    Input('country-dropdown', 'value')
)
def update_country_plots(country):
    """Uppdaterar alla land-specifika visualiseringar"""
    
    # Top sports
    top_sports = analyzer.top_sports_by_medals(country)
    top_sports_df = top_sports.reset_index()
    top_sports_df.columns = ['Sport', 'Medals']
    fig1 = px.bar(
        top_sports_df,
        x='Medals',
        y='Sport',
        orientation='h',
        color='Medals',
        color_continuous_scale='viridis',  # Color-blind friendly palette - Plotly Express
        title=f'{country} - Top {len(top_sports)} sporter med flest medaljer',
        labels={'Medals': 'Antal medaljer', 'Sport': 'Sport'}
    )
    fig1.update_layout(
        showlegend=False,
        xaxis_title="Antal medaljer",
        yaxis_title="Sport (rankad efter medaljer)",
        coloraxis_colorbar=dict(title="Medaljer")
    )
    
    # Medals per Olympics
    medals_year = analyzer.medals_per_olympics(country)
    medals_year_df = medals_year.reset_index()
    medals_year_df.columns = ['Year', 'Medals']
    fig2 = px.line(
        medals_year_df,
        x='Year',
        y='Medals',
        markers=True,
        title=f'{country} - Medaljer per OS',
        labels={'Year': 'År', 'Medals': 'Antal medaljer'}
    )
    fig2.update_traces(
        mode='lines+markers',
        line=dict(color='#264653', width=3),
        marker=dict(size=8, color='#E9C46A', line=dict(color='#264653', width=1))
    )
    fig2.update_layout(
        showlegend=False,
        xaxis_title="Olympiskt år",
        yaxis_title="Antal medaljer"
    )
    
    # Age histogram
    ages = analyzer.age_distribution(country)
    fig3 = px.histogram(
        ages, 
        nbins=30, 
        color_discrete_sequence=['#2A9D8F'],
        title=f'{country} - Åldersfördelning',
        labels={'value': 'Ålder', 'count': 'Antal idrottare'}
    )
    fig3.update_layout(
        bargap=0.1,
        xaxis_title="Ålder (år)",
        yaxis_title="Antal idrottare"
    )
    
    # Medal types
    medal_stats = analyzer.get_medal_statistics(country)
    fig4 = px.pie(
        values=medal_stats.values,
        names=medal_stats.index,
        title=f'{country} - Fördelning av medaljtyper',
        color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'}
    )
    fig4.update_layout(legend_title_text="Medaljtyp")
    
    return fig1, fig2, fig3, fig4


@app.callback(
    [Output('sport-medals', 'figure'),
     Output('sport-ages', 'figure'),
     Output('sport-gender', 'figure'),
     Output('sport-medal-types', 'figure')],
    Input('sport-dropdown', 'value')
)
def update_sport_plots(sport):
    """Uppdaterar alla sport-specifika visualiseringar"""
    
    if not sport:
        # Returnera tomma figurer om ingen sport vald
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="Välj en sport", showarrow=False)
        return empty_fig, empty_fig, empty_fig, empty_fig
    
    analysis = analyzer.sport_analysis(sport)
    
    # Medal distribution by country
    medal_countries = analysis['medal_countries'].head(10)
    fig1 = px.bar(
        x=medal_countries.values,
        y=medal_countries.index,
        orientation='h',
        title=f'{sport} - Medaljer per land (Top 10)',
        labels={'x': 'Antal medaljer', 'y': 'Land (NOC)'},
        color=medal_countries.values,
        color_continuous_scale='viridis'
    )
    fig1.update_layout(
        showlegend=False,
        xaxis_title="Antal medaljer",
        yaxis_title="Land (NOC)",
        coloraxis_colorbar=dict(title="Medaljer")
    )
    
    # Age distribution
    age_dist = analysis['age_distribution']
    fig2 = px.histogram(
        age_dist, 
        nbins=25,
        title=f'{sport} - Åldersfördelning',
        labels={'value': 'Ålder', 'count': 'Antal idrottare'},
        color_discrete_sequence=['#E76F51']
    )
    fig2.update_layout(
        bargap=0.12,
        xaxis_title="Ålder (år)",
        yaxis_title="Antal idrottare"
    )
    
    # Gender split
    gender_split = analysis['gender_split']
    fig3 = px.pie(
        values=gender_split.values,
        names=gender_split.index,
        title=f'{sport} - Könsfördelning',
        color_discrete_map={'M': '#4ECDC4', 'F': '#FF6B6B'}
    )
    fig3.update_layout(legend_title_text="Kön")
    
    # Medal types
    medal_types = analysis['medal_types']
    fig4 = px.pie(
        values=medal_types.values,
        names=medal_types.index,
        title=f'{sport} - Fördelning av medaljtyper',
        color_discrete_map={'Gold': '#FFD700', 'Silver': '#C0C0C0', 'Bronze': '#CD7F32'}
    )
    fig4.update_layout(legend_title_text="Medaljtyp")
    
    return fig1, fig2, fig3, fig4


@app.callback(
    Output('canada-3d-profile', 'figure'),
    [
        Input('canada-season-filter', 'value'),
        Input('canada-medal-filter', 'value'),
        Input('canada-year-range', 'value')
    ]
)
def update_canada_3d(season, medal_filter, year_range):
    """Interaktiv 3D-visualisering för Kanada."""
    medal_only = medal_filter == 'medal'
    profile_df = analyzer.country_athlete_profile('CAN', season=season, medal_only=medal_only)

    if year_range:
        start_year, end_year = year_range
        profile_df = profile_df[(profile_df['Year'] >= start_year) & (profile_df['Year'] <= end_year)]

    if profile_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="Ingen data för de valda filtren.", showarrow=False, font=dict(size=16))
        fig.update_layout(
            title="Kanada – 3D-profil",
            scene=dict(
                xaxis_title="Ålder (år)",
                yaxis_title="Längd (cm)",
                zaxis_title="Vikt (kg)"
            )
        )
        return fig

    color_dimension = 'Medal' if medal_only else 'Sport'
    hover_fields = {
        'Sport': True,
        'Event': True,
        'Year': True,
        'Season': True,
        'Medal': True,
        'Sex': True
    }

    fig = px.scatter_3d(
        profile_df,
        x='Age',
        y='Height',
        z='Weight',
        color=color_dimension,
        size='Age',
        hover_data=hover_fields,
        animation_frame='Year',
        animation_group='ID',
        title="Kanada – Atletprofil i 3D över tid",
        labels={
            'Age': 'Ålder (år)',
            'Height': 'Längd (cm)',
            'Weight': 'Vikt (kg)'
        }
    )

    fig.update_layout(
        scene=dict(
            xaxis_title="Ålder (år)",
            yaxis_title="Längd (cm)",
            zaxis_title="Vikt (kg)"
        ),
        legend_title_text="Medaljtyp" if medal_only else "Sport",
        margin=dict(l=0, r=0, b=0, t=60)
    )

    return fig


@app.callback(
    Output('global-medal-race', 'figure'),
    [
        Input('global-season-filter', 'value'),
        Input('global-top-n-slider', 'value')
    ]
)
def update_global_medal_race(season, top_n):
    """Animerad global medaljtabell."""
    data = analyzer.global_medal_race(season=season, top_n=top_n)

    if data.empty:
        fig = go.Figure()
        fig.add_annotation(text="Ingen medaljstatistik för de valda inställningarna.", showarrow=False)
        fig.update_layout(title="Global medaljtabell")
        return fig

    fig = px.bar(
        data,
        x='Medals',
        y='NOC',
        color='NOC',
        animation_frame='Year',
        orientation='h',
        title="Global medaljtabell – år för år",
        labels={
            'Medals': 'Antal medaljer',
            'NOC': 'Land (NOC)',
            'Year': 'År'
        },
        category_orders={'Year': sorted(data['Year'].unique())}
    )

    max_medals = int(data['Medals'].max()) if not data['Medals'].empty else 5
    fig.update_layout(
        xaxis_title="Antal medaljer",
        yaxis_title="Land (NOC)",
        legend_title_text="Land",
        xaxis=dict(range=[0, max_medals + 2])
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

