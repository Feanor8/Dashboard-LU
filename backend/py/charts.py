import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def pie_chart_from_column(df, column_name, top_n=8, title=""):
    # defensive checks
    if column_name not in df.columns or df.shape[0] == 0:
        fig = go.Figure()
        fig.update_layout(title=f"Keine Daten für {column_name} verfügbar")
        return fig

    counts = df[column_name].fillna("keine Angabe").value_counts()

    # Top N, sum up rest
    if len(counts) > top_n:
        top = counts.nlargest(top_n)
        others = counts.drop(top.index).sum()
        counts = top.append(pd.Series({"Andere": others}))

    # pie-chart (with plotly)
    fig = px.pie(
        names=counts.index,
        values=counts.values,
        #title=title or f"{column_name} Verteilung", / Don't use it with app.py
    )
    fig.update_traces(textinfo="percent+label", textposition="inside")
    fig.update_layout(margin=dict(t=40, b=10, l=10, r=10), legend_title_text=None)

    return fig

def election_bar_chart(
    df,
    party_col="Partei",
    value_col=None,
    top_n=12,
    title="Wahlergebnis"
):
    # Farb-Mapping (wie du schon hattest)
    party_colors = {
        "CDU/CSU": "#000000",
        "CSU": "#008AC5",
        "SPD": "#E3000F",
        "FDP": "#FFED00",
        "AfD": "#009EE0",
        "Grüne": "#1AA037",
        "BSW": "#7E234F",
        "Bündnis 90/Die Grünen": "#1AA037",
        "Die Linke": "#BE3075",
        "LINKE": "#BE3075",
        "Freie Wähler": "#FF8C00",
        "PIRATEN": "#FF8800",
        "Andere": "#C0C0C0",
        "Sonstige": "#A0A0A0",
    }
    default_color = "#888888"

    # Guard: Spalte / Daten prüfen
    if party_col not in df.columns or df.shape[0] == 0:
        fig = go.Figure()
        fig.update_layout(title=f"Keine Daten für {party_col} verfügbar")
        return fig

    # Auto-Finden der value_col wie gehabt
    if value_col is None:
        candidates = ["Stimmen_Prozent", "Stimmen", "Prozent", "Votes", "Anzahl"]
        found = [c for c in candidates if c in df.columns]
        if found:
            value_col = found[0]
        else:
            nums = [c for c in df.columns if c != party_col and pd.api.types.is_numeric_dtype(df[c])]
            value_col = nums[0] if nums else None

    if value_col is None or value_col not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="Keine geeignete Wertespalte gefunden")
        return fig

    # Datenkopie + bereinigung
    d = df[[party_col, value_col]].copy()
    d[party_col] = d[party_col].fillna("keine Angabe")
    d[value_col] = pd.to_numeric(d[value_col], errors="coerce").fillna(0)

    # Prozent-Check
    is_percent = (
        "prozent" in value_col.lower() or 
        (0 < d[value_col].max() <= 100)
    )

    # Sortieren (absteigend nach Wert)
    d = d.sort_values(by=value_col, ascending=False).reset_index(drop=True)

    # Top N + "Andere"
    if d.shape[0] > top_n:
        top = d.iloc[:top_n]
        others_sum = d.iloc[top_n:][value_col].sum()
        d_plot = pd.concat([
            top,
            pd.DataFrame([{party_col: "Andere", value_col: others_sum}])
        ], ignore_index=True)
    else:
        d_plot = d

    # color map nur für sichtbare Einträge
    unique_parties = d_plot[party_col].astype(str).tolist()
    color_map = {p: party_colors.get(p, default_color) for p in unique_parties}

    # CATEGORY ORDER erzwingen (wichtig für korrekte Textzuordnung)
    category_orders = {party_col: unique_parties}

    # Plotly: Übergib text als numerische Spalte, setze category_orders, color_discrete_map
    fig = px.bar(
        d_plot,
        x=party_col,
        y=value_col,
        text=value_col,                      # <--- numerische Werte direkt
        color=party_col,
        color_discrete_map=color_map,
        category_orders=category_orders,     # <--- zwingt Plotly, die Reihenfolge beizubehalten
        labels={party_col: "Partei", value_col: ("Prozent" if is_percent else "Stimmen")},
    )

    # Formatierte Text-Labels sauber per texttemplate setzen
    if is_percent:
        fig.update_traces(texttemplate='%{text:.1f} %', textposition="outside")
        fig.update_layout(yaxis=dict(ticksuffix=" %"))
    else:
        # Tausender-Trenner (Punkte)
        fig.update_traces(texttemplate='%{text:,}', textposition="outside")
        # Plotly standard-Formatstring setzt Kommas; wir wollen Punkte — alternativ formatiere strings vorher
        # Wenn du zwingend Punkte statt Kommas willst, setze text to formatted strings:
        # d_plot["_text"] = d_plot[value_col].map(lambda v: f"{int(v):,}".replace(",", "."))
        # fig.update_traces(text=d_plot["_text"], textposition="outside")
        fig.update_layout(yaxis_tickformat=",")

    fig.update_layout(
        margin=dict(t=40, b=40, l=10, r=10),
        xaxis_tickangle=-30,
        showlegend=False,
        title=title or ""
    )

    return fig