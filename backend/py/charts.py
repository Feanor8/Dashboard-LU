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