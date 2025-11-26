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
CSV_PATH_ELECTIONS = os.path.join(os.path.dirname(__file__), 'data', 'wahlen.csv')

 
def create_figure_for_mapping(df, mapping):
    # (deine vorhandene Implementierung unverändert)
    if isinstance(mapping, str):
        return chart.pie_chart_from_column(df, mapping, top_n=8, title=mapping)

    if isinstance(mapping, dict):
        t = mapping.get("type", "pie").lower()
        col = mapping.get("col") or mapping.get("column")
        top_n = mapping.get("top_n", 8)

        if t == "pie":
            return chart.pie_chart_from_column(df, col, top_n=top_n, title=mapping.get("title",""))
        elif t in ("bar", "election", "election_bar"):
            return chart.election_bar_chart(
                df,
                party_col=col,
                value_col=mapping.get("value_col"),
                top_n=mapping.get("top_n", 12),
                title=mapping.get("title", "")
            )
        else:
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.update_layout(title=f"Unbekannter Chart-Typ: {t}")
            return fig

    import plotly.graph_objects as go
    fig = go.Figure()
    fig.update_layout(title="Ungültige Chart-Definition")
    return fig
@app.route('/')
def index():
    df = pd.read_csv(CSV_PATH_KOSIS)
    df_el = pd.read_csv(CSV_PATH_ELECTIONS)

    # sources-Mapping: name -> DataFrame ( DB-Handler etc. sein)
    sources = {
        "kosis": df,
        "elections": df_el,
        # "other": load_other_source(), ...
    }

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

    
    # Mapping: DOM-ID -> Spaltenname von CSV oder Datenbankspalte (oder Funktion)
    charts_map = {
    "family_pie": "einFamiliebestand",     # default: pie
    "religion_pie": {"type": "pie", "col": "Religion", "top_n": 8, "source": "kosis"},
    "migra_pie": {"type": "pie", "col": "Religion", "source": "kosis"},
    "migra_pie_country": {"type": "pie", "col": "Religion", "top_n": 10, "source": "kosis"},
    "private_households": {"type": "pie", "col": "Religion", "source": "kosis"},
    "apartments": {"type": "pie", "col": "Religion", "source": "kosis"},
    "sinus_milieus": {"type": "pie", "col": "Religion", "source": "kosis"},
    "latest_election": {"type": "bar", "col": "Partei", "value_col": "Stimmen_Prozent", "top_n": 12, "source": "elections"},    # weitere Karten...
    }

    graphs = {}
    for dom_id, mapping in charts_map.items():
        # Ermittle die Quelle (default 'kosis')
        source_name = None
        if isinstance(mapping, dict):
            source_name = mapping.get("source")
        # Wenn mapping ist nur String, du kannst optional eine Default-Quelle definieren:
        if source_name is None:
            source_name = "kosis"

        used_df = sources.get(source_name)
        if used_df is None:
            # Falls Quelle fehlt: erstelle leere Figure mit Hinweis
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.update_layout(title=f"Keine Datenquelle '{source_name}' gefunden")
        else:
            fig = create_figure_for_mapping(used_df, mapping)

        graphs[dom_id] = fig.to_dict()

    graphs_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', stats=stats, graphs_json=graphs_json)
