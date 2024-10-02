import streamlit as st
from utils import (
    create_situation,
    calculate_ctc,
    YEAR,
    TEAL_ACCENT,
    MAX_INCOME,
)
from graph import create_reform_comparison_graph
from config import (
    REFORMS,
    APP_TITLE,
    BASELINE_DESCRIPTION,
    REFORMS_DESCRIPTION,
    NOTES,
)

import yaml


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="👪", layout="wide")
    st.title(APP_TITLE)

    st.markdown(BASELINE_DESCRIPTION)

    # User inputs
    is_married = st.checkbox("I'm married")
    num_children = st.number_input(
        "Number of children", min_value=0, max_value=10, value=1
    )
    child_ages = [
        st.number_input(
            f"Age of child {i+1}", min_value=0, max_value=16, value=5
        )
        for i in range(num_children)
    ]
    earnings = st.number_input(
        f"Household wages and salaries in {YEAR}",
        min_value=0,
        value=50000,
        step=1000,
        max_value=MAX_INCOME,
    )

    if st.button("Calculate My CTC"):
        household = create_situation(is_married, child_ages, earnings)
        baseline_ctc = calculate_ctc(household, "baseline")

        st.markdown(
            f"<h2 style='text-align: center;'>In {YEAR}, you are eligible for a "
            f"<span style='color:{TEAL_ACCENT};'>${baseline_ctc:,.0f}</span> child tax credit.</h2>",
            unsafe_allow_html=True,
        )

        st.markdown("## How would reforms affect your child tax credit?")
        st.markdown(REFORMS_DESCRIPTION)

        results = calculate_ctc_for_reforms(household)
        fig = create_reform_comparison_graph(results)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## Impact of Reforms")
        for reform_name, ctc_value in results.items():
            if reform_name != "Baseline":
                diff = ctc_value - baseline_ctc
                change = "increase" if diff > 0 else "decrease"
                st.markdown(
                    f"- The **{reform_name}** reform would {change} your child tax credit by **${abs(diff):,.0f}**."
                )

    st.markdown(NOTES)


def calculate_ctc_for_reforms(household):
    return {
        reform_name: calculate_ctc(household, reform_key)
        for reform_key, reform_name in REFORMS
    }


if __name__ == "__main__":
    main()
