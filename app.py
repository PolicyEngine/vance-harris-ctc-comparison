import streamlit as st
import plotly.graph_objects as go
from policyengine_core.charts import format_fig
import pandas as pd
from utils import (
    LIGHT_GRAY,
    DARK_RED,
    LIGHT_RED,
    BLUE,
    create_situation,
    calculate_ctc,
    MAX_INCOME,
    YEAR,
    TEAL_ACCENT,
)

import yaml


def create_reform_comparison_graph(df):
    colors = {
        "Baseline": LIGHT_GRAY,
        "Harris": BLUE,
        "Vance (refundable)": DARK_RED,
        "Vance (non-refundable)": LIGHT_RED,
    }

    # Sort the dataframe by CTC value in descending order
    df_sorted = df.sort_values(by="ctc", ascending=False)

    fig = go.Figure()

    baseline_value = df_sorted[df_sorted["reform"] == "Baseline"][
        "ctc"
    ].values[0]

    for reform in df_sorted["reform"]:
        value = df_sorted[df_sorted["reform"] == reform]["ctc"].values[0]
        diff = value - baseline_value

        text_inside = f"${value:,.0f}"
        text_outside = ""
        if reform != "Baseline":
            text_outside = f"+${diff:,.0f}" if diff > 0 else f"-${-diff:,.0f}"

        fig.add_trace(
            go.Bar(
                y=[reform],
                x=[value],
                name=reform,
                orientation="h",
                marker_color=colors.get(reform, LIGHT_GRAY),
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
        title=dict(
            text="How reforms would affect your child tax credit",
            font=dict(size=24),
        ),
        xaxis=dict(tickformat="$,.0f", tickfont=dict(size=14)),
        height=500,
        width=800,
        bargap=0.2,
        uniformtext_minsize=10,
        uniformtext_mode="hide",
        showlegend=False,
        yaxis=dict(title=None, tickfont=dict(size=14)),
        font=dict(size=14),
    )

    return fig


# Streamlit app
st.title("Child Tax Credit Calculator")

# User inputs
is_married = st.checkbox("Married household")
num_children = st.number_input(
    "Number of children", min_value=0, max_value=10, value=1
)
child_ages = [
    st.number_input(f"Age of child {i+1}", min_value=0, max_value=16, value=5)
    for i in range(num_children)
]
earnings = st.number_input(
    f"Household wages and salaries in {YEAR}",
    min_value=0,
    max_value=int(MAX_INCOME),
    value=50000,
    step=1000,
)

if st.button("Generate Comparison"):
    # Create placeholders for headline and chart
    headline_placeholder = st.empty()
    chart_placeholder = st.empty()

    # Create the household dictionary
    household = create_situation(is_married, child_ages, earnings)

    # List of reforms to calculate with their display names
    reforms = [
        ("baseline", "Baseline"),
        ("harris", "Harris"),
        ("vance_non_refundable", "Vance (non-refundable)"),
        ("vance_refundable", "Vance (refundable)"),
    ]

    # Initialize an empty list to store the data
    data = []

    # Iterate through reforms
    for reform_key, reform_name in reforms:
        # Calculate CTC for the current reform
        ctc_value = calculate_ctc(household, reform_key)

        # Add the result to the data list
        data.append(
            {"reform": reform_name, "ctc": ctc_value, "earnings": earnings}
        )

        # Create a new DataFrame from the data list
        df = pd.DataFrame(data)

        # Update the headline and chart
        if reform_key == "baseline":
            headline_placeholder.markdown(
                f"<h1 style='text-align: center;'>In {YEAR}, you are eligible for a <br><span style='color:{TEAL_ACCENT};'>${ctc_value:,.0f}</span> child tax credit.</h1>",
                unsafe_allow_html=True,
            )

        fig = create_reform_comparison_graph(df)
        chart_placeholder.plotly_chart(format_fig(fig))

st.write(
    f"""
### Notes:
- All earnings are from the tax filer's wages and salaries in {YEAR}.
- The filer has no other taxable income.
- The filer takes the standard deduction.
- Married couples file jointly.
- We assume Senator JD Vance's suggestion has the same age limit as the current CTC.
"""
)
