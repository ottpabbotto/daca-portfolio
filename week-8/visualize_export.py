import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_weekly_chart(df_weekly):
    """
    Loob nädalase käibe trendi näitava joondiagrammi.

    Nädalane koondandmestik kasutab kuupäeva 'sale_date'
    indeksina. Diagrammi jaoks teisendatakse indeks ajutiselt
    tavaliseks veeruks.

    Parameetrid:
        df_weekly (pd.DataFrame):
            Nädalaste koondnäitajatega DataFrame.
            Eeldatav indeks on 'sale_date' ja käibe veerg
            on 'revenue'.

    Tagastab:
        plotly.graph_objects.Figure:
            Plotly joondiagrammi objekt.
    """

    # Teeme koopia, et algset transform.py tulemust mitte muuta.
    chart_data = df_weekly.reset_index()

    # Loome nädalase käibe trendi joondiagrammi.
    fig = px.line(
        chart_data,
        x="sale_date",
        y="revenue",
        title="UrbanStyle: Nädalane käivetrend",
        labels={
            "sale_date": "Nädala lõpp",
            "revenue": "Käive (EUR)"
        },
        template="plotly_white"
    )

    # Kohandame joone UrbanStyle'i brändivärvi ja paksusega.
    fig.update_traces(
        line_color="#009B8D",
        line_width=3
    )

    return fig


def create_kpi_summary(kpis):
    """
    Loob kolme peamise KPI näidiskaardid.

    Kuvatakse:
        - Kogutulu
        - Klientide arv
        - Keskmine tellimusväärtus (AOV)

    Parameetrid:
        kpis (dict):
            Sõnastik KPI väärtustega.

    Tagastab:
        plotly.graph_objects.Figure:
            Plotly KPI-kaartide objekt.
    """

    # Loome kolme indikaatoriga paigutuse.
    fig = make_subplots(
        rows=1,
        cols=3,
        specs=[[
            {"type": "indicator"},
            {"type": "indicator"},
            {"type": "indicator"}
        ]]
    )

    # Kuvame ettevõtte kogutulu.
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis.get("total_revenue", 0),
            title={"text": "Kogutulu (EUR)"},
            number={"font": {"color": "#1A1A2E"}},
            domain={"row": 0, "column": 0}
        ),
        row=1,
        col=1
    )

    # Kuvame klientide arvu.
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis.get("unique_customers", 0),
            title={"text": "Klientide arv"},
            number={"font": {"color": "#1A1A2E"}},
            domain={"row": 0, "column": 1}
        ),
        row=1,
        col=2
    )

    # Kuvame keskmise tellimuse väärtuse.
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=kpis.get("avg_order_value", 0),
            title={"text": "AOV (EUR)"},
            number={"font": {"color": "#1A1A2E"}},
            domain={"row": 0, "column": 2}
        ),
        row=1,
        col=3
    )

    # Määrame KPI-kaartide üldise kujunduse.
    fig.update_layout(
        height=300,
        template="plotly_white"
    )

    return fig


def export_results(df, output_dir, figs=None):
    """
    Ekspordib analüüsi tulemused CSV- ja HTML-failidena.

    Funktsioon loob väljundkausta juhul, kui seda veel ei ole.
    CSV-failile ja diagrammidele lisatakse kuupäev, et säilitada
    erinevate analüüsikäivituste ajalugu.

    Parameetrid:
        df (pd.DataFrame):
            Eksporditav andmetabel.

        output_dir (str):
            Kaust, kuhu tulemused salvestatakse.

        figs (list, optional):
            Plotly diagrammide nimekiri, mis salvestatakse
            HTML-failidena.
    """

    # Loome väljundkausta, kui seda veel ei eksisteeri.
    os.makedirs(output_dir, exist_ok=True)

    # Genereerime failinimedes kasutatava kuupäeva.
    date_str = datetime.now().strftime("%Y%m%d")

    # Salvestame analüüsi tulemused CSV-failina.
    csv_filename = f"rfm_results_{date_str}.csv"
    csv_path = os.path.join(output_dir, csv_filename)

    df.to_csv(csv_path, index=False)

    print(f"Andmed salvestatud: {csv_path}")

    # Kui diagrammid on olemas, salvestame need HTML-failidena.
    if figs:
        for idx, fig in enumerate(figs):
            html_filename = f"chart_{idx}_{date_str}.html"
            html_path = os.path.join(output_dir, html_filename)

            fig.write_html(html_path)

            print(f"Diagramm salvestatud: {html_path}")


if __name__ == "__main__":
    """
    Testib visualiseerimise ja ekspordi funktsioone näidisandmetega.
    """

    # Loome näidisandmed nädalase käibe diagrammi testimiseks.
    weekly_data = pd.DataFrame({
        "sale_date": ["W1", "W2", "W3", "W4"],
        "revenue": [12500, 13800, 14900, 17800]
    })

    # Loome näidisandmed KPI-kaartide testimiseks.
    kpi_values = {
        "total_revenue": 59000,
        "unique_customers": 1250,
        "avg_order_value": 47.2
    }

    # Loome nädalase käibe diagrammi.
    weekly_fig = create_weekly_chart(weekly_data)

    # Loome KPI-kaartide visualiseeringu.
    kpi_fig = create_kpi_summary(kpi_values)

    # Ekspordime näidisandmed ja loodud diagrammid output-kausta.
    export_results(
        weekly_data,
        "output",
        figs=[weekly_fig, kpi_fig]
    )