from flask import Flask, render_template
import pandas as pd
import os
import py.stat as stat   # Alle Statistik als numerischer Wert
import py.charts as chart
import plotly
import plotly.express as px
import json


app = Flask(__name__)

CSV_PATH_KOSIS = os.path.join(os.path.dirname(__file__), 'data', 'k500.csv')

@app.route('/')
def index():
    df = pd.read_csv(CSV_PATH_KOSIS)

    stats = {
        "gesamt": stat.num_population(df),
        "hauptwohnsitz": stat.num_population_main_household(df),
        "sekundärwohnsitz": stat.num_population_secondary_household(df),
        "anteil_maennlich": stat.per_population_male(df),
        "anteil_weiblich": stat.per_population_female(df),
        "altersdurchschnitt": stat.num_population_average_age(df),
        "hinzugezogen": stat.num_population_moved_in(df),
        "fortgezogen": stat.num_population_moved_out(df),
        "zuzug_saldo": stat.diff_population_moved(df),
        "geburten": stat.num_population_births(df),
        "tode": stat.num_population_deaths(df),
        "geburten_saldo": stat.diff_population_births_and_deaths(df),
        "sopf_beschäftigte": stat.num_population_social_insurance_subject(df),
        "beschäftigung_prozent": stat.per_population_with_jobs(df),
        "arbeitslose_nummer": stat.num_population_no_jobs(df),
        "arbeitslose_prozent": stat.per_population_no_jobs(df),
        "kaufkraft_person": stat.num_population_buying_average_person(df),
        "kaufkraft_haushalt": stat.num_population_buying_average_household(df),
        "kaufkraft_person_index": stat.num_population_buying_index_person(df),
        "kaufkraft_haushalt_index": stat.num_population_buying_index_household(df)
    }

    html = {
        
    }
    
    # Mapping: DOM-ID -> Spaltenname von CSV oder Datenbankspalte (oder Funktion)
    charts_map = {
        "family_pie": "einFamiliebestand",
        "religion_pie": "Religion",
        "migra_pie": "Religion",
        "migra_pie_country": "Religion",
        "private_households": "Religion",
        "apartments": "Religion",
        "sinusmilieus": "Religion",
        "latest_election": "Religion"
    }

    graphs = {}
    for dom_id, col in charts_map.items():
        fig = chart.pie_chart_from_column(df, col, top_n=8, title=col)
        graphs[dom_id] = fig.to_dict()

    graphs_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('index.html', stats=stats, graphs_json=graphs_json)