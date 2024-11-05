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


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="👪")
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

        # Calculate baseline CTC first
        baseline_ctc = calculate_ctc(household, "baseline")

        # Display the baseline CTC
        st.markdown(
            f"<h2 style='text-align: center;'>In {YEAR}, you will be eligible for a "
            f"<span style='color:{TEAL_ACCENT};'>${baseline_ctc:,.0f}</span> child tax credit.</h2>",
            unsafe_allow_html=True,
        )

        st.markdown(REFORMS_DESCRIPTION)

        # Create placeholders for the chart and results
        chart_placeholder = st.empty()

        results = {"Baseline": baseline_ctc}

        # Update chart with baseline
        fig = create_reform_comparison_graph(results)
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # Calculate and display other reforms
        for reform_key, reform_name in REFORMS[
            1:
        ]:  # Skip baseline as it's already calculated
            ctc_value = calculate_ctc(household, reform_key)
            results[reform_name] = ctc_value

            # Update the chart
            fig = create_reform_comparison_graph(results)
            chart_placeholder.plotly_chart(fig, use_container_width=True)

    st.markdown(NOTES)


if __name__ == "__main__":
    main()
