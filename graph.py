import plotly.graph_objects as go
import pandas as pd
from utils import GRAY, DARK_RED, LIGHT_RED, BLUE
import yaml


def create_reform_comparison_graph(results):
    colors = {
        "Baseline": GRAY,
        "Harris": BLUE,
        "Vance (refundable)": DARK_RED,
        "Vance (non-refundable)": LIGHT_RED,
    }

    df = pd.DataFrame([{"reform": k, "ctc": v} for k, v in results.items()])
    df_sorted = df.sort_values(by="ctc", ascending=False)

    fig = go.Figure()

    if "Baseline" in results:
        baseline_value = results["Baseline"]

        for reform, value in zip(df_sorted["reform"], df_sorted["ctc"]):
            diff = value - baseline_value
            text_inside = f"${value:,.0f}"
            text_outside = (
                f"+${diff:,.0f}"
                if diff > 0
                else f"-${-diff:,.0f}" if diff < 0 else ""
            )

            fig.add_trace(
                go.Bar(
                    y=[reform],
                    x=[value],
                    name=reform,
                    orientation="h",
                    marker_color=colors.get(reform, GRAY),
                    text=text_inside,
                    textposition="inside",
                    insidetextanchor="middle",
                    textfont=dict(size=16, color="white"),
                )
            )

            if text_outside:
                fig.add_annotation(
                    y=reform,
                    x=value,
                    text=text_outside,
                    showarrow=False,
                    xanchor="left",
                    yanchor="middle",
                    xshift=5,
                    font=dict(size=16),
                )

    fig.update_layout(
        title=dict(text="Comparison of CTC Reforms", font=dict(size=24)),
        xaxis=dict(
            title="Child Tax Credit Amount",
            tickformat="$,.0f",
            tickfont=dict(size=14),
        ),
        height=400,
        bargap=0.2,
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        showlegend=False,
        yaxis=dict(title=None, tickfont=dict(size=14)),
        font=dict(size=14),
        margin=dict(l=20, r=20, t=40, b=20),
    )

    return fig