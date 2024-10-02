import plotly.graph_objects as go
import pandas as pd
from utils import GRAY
from config import COLOR_MAP
import yaml


def create_reform_comparison_graph(results):
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

            # Define pattern fill for Vance suggestions
            pattern = None
            text_color = "white"
            if "Vance suggestion" in reform:
                pattern = dict(
                    shape="/",
                    solidity=0.7,
                    size=10,
                    bgcolor="white",
                )
                text_color = "black"

            fig.add_trace(
                go.Bar(
                    y=[reform],
                    x=[value],
                    name=reform,
                    orientation="h",
                    marker=dict(
                        color=COLOR_MAP.get(reform, GRAY),
                        pattern=pattern,
                    ),
                    text=text_inside,
                    textposition="inside",
                    insidetextanchor="middle",
                    textfont=dict(size=18, color=text_color),
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
        title=dict(
            text="Your 2025 Child Tax Credit by Policy", font=dict(size=24)
        ),
        xaxis=dict(
            title=None,
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
