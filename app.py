import streamlit as st
import numpy as np
import plotly.graph_objects as go
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from policyengine_core.charts import format_fig
import plotly.express as px

# Define the reforms (unchanged)
vance_ref = Reform.from_dict({
  "gov.irs.credits.ctc.amount.base[0].amount": {
    "2024-01-01.2100-12-31": 5000
  },
  "gov.irs.credits.ctc.phase_out.amount": {
    "2024-01-01.2100-12-31": 0
  },
  "gov.irs.credits.ctc.refundable.fully_refundable": {
    "2024-01-01.2100-12-31": True
  }
}, country_id="us")

vance_non_ref = Reform.from_dict({
  "gov.irs.credits.ctc.amount.base[0].amount": {
    "2024-01-01.2100-12-31": 5000
  },
  "gov.irs.credits.ctc.phase_out.amount": {
    "2024-01-01.2100-12-31": 0
  }
}, country_id="us")

reform_harris = Reform.from_dict({
  "gov.contrib.congress.delauro.american_family_act.baby_bonus": {
    "2024-01-01.2100-12-31": 2400
  },
  "gov.irs.credits.ctc.amount.arpa[0].amount": {
    "2023-01-01.2028-12-31": 3600
  },
  "gov.irs.credits.ctc.amount.arpa[1].amount": {
    "2023-01-01.2028-12-31": 3000
  },
  "gov.irs.credits.ctc.phase_out.arpa.in_effect": {
    "2023-01-01.2028-12-31": True
  },
  "gov.irs.credits.ctc.refundable.fully_refundable": {
    "2023-01-01.2028-12-31": True
  }
}, country_id="us")

YEAR = "2025"
DEFAULT_AGE = 40
MAX_INCOME = 500000

def create_situation(filing_status, child_ages, earnings):
    situation = {
        "people": {
            "adult": {
                "age": {YEAR: DEFAULT_AGE},
                "employment_income": {YEAR: earnings},
            },
        },
        "families": {"family": {"members": ["adult"]}},
        "marital_units": {"marital_unit": {"members": ["adult"]}},
        "tax_units": {
            "tax_unit": {
                "members": ["adult"],
                # Performance improvement settings
                "premium_tax_credit": {YEAR: 0},
                "tax_unit_itemizes": {YEAR: False},
                "taxable_income_deductions_if_itemizing": {YEAR: 0},
                "alternative_minimum_tax": {YEAR: 0},
                "net_investment_income_tax": {YEAR: 0},
                "eitc": {YEAR: 0},
            }
        },
        "households": {
            "household": {"members": ["adult"], "state_name": {YEAR: "TX"}}
        },
    }
    
    for i, age in enumerate(child_ages):
        child_id = f"child_{i}"
        situation["people"][child_id] = {"age": {YEAR: age}}
        for unit in ["families", "tax_units", "households"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(child_id)
    
    if filing_status == "married":
        situation["people"]["spouse"] = {"age": {YEAR: DEFAULT_AGE}}
        for unit in ["families", "marital_units", "tax_units", "households"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append("spouse")
        
    return situation

def calculate_ctc(situation, reform=None):
    simulation = Simulation(situation=situation, reform=reform)
    if reform is None:
        return simulation.calculate("ctc_value", YEAR)[0]
    else:
        return simulation.calculate("ctc", YEAR)[0]

def create_reform_comparison_graph(filing_status, child_ages, earnings):
    colors = {
        "vance_ref": "#18375f",   # Dark blue
        "vance_non_ref": "#2976fe", # Light blue
        "harris": "#c5c5c5",      # Light gray
    }
    
    situation = create_situation(filing_status, child_ages, earnings)
    baseline_ctc = calculate_ctc(situation)
    vance_ref_ctc = calculate_ctc(situation, vance_ref)
    vance_non_ref_ctc = calculate_ctc(situation, vance_non_ref)
    harris_ctc = calculate_ctc(situation, reform_harris)
    
    reforms = ["Vance (Refundable)", "Vance (Non-Refundable)", "Harris"]
    ctc_impacts = [
        vance_ref_ctc - baseline_ctc,
        vance_non_ref_ctc - baseline_ctc,
        harris_ctc - baseline_ctc
    ]
    
    fig = px.bar(
        x=reforms,
        y=ctc_impacts,
        color=reforms,
        color_discrete_map={
            "Vance (Refundable)": colors["vance_ref"],
            "Vance (Non-Refundable)": colors["vance_non_ref"],
            "Harris": colors["harris"]
        },
        labels={"x": "Reform", "y": "CTC Impact"},
        title=f'CTC Impact Comparison for {"Married" if filing_status == "married" else "Single"} Household (Earnings: ${earnings:,})'
    )
    
    fig.update_layout(
        yaxis_title="CTC Impact (Reformed - Baseline)",
        yaxis=dict(tickformat='$,.0f'),
        showlegend=False,
        height=400,
        width=800,
    )
    
    return fig

def create_reform_comparison_line_graph(filing_status, child_ages):
    colors = {
        "vance_ref": "#18375f",   # Dark blue
        "vance_non_ref": "#2976fe", # Light blue
        "harris": "#c5c5c5",      # Light gray
    }
    
    x = np.linspace(0, MAX_INCOME, 501)
    fig = go.Figure()
    
    for earnings in x:
        situation = create_situation(filing_status, child_ages, earnings)
        baseline_ctc = calculate_ctc(situation)
        vance_ref_ctc = calculate_ctc(situation, vance_ref)
        vance_non_ref_ctc = calculate_ctc(situation, vance_non_ref)
        harris_ctc = calculate_ctc(situation, reform_harris)
        
        fig.add_trace(go.Scatter(x=[earnings], y=[vance_ref_ctc - baseline_ctc], mode='lines', line=dict(color=colors['vance_ref']), name='Vance (Refundable)'))
        fig.add_trace(go.Scatter(x=[earnings], y=[vance_non_ref_ctc - baseline_ctc], mode='lines', line=dict(color=colors['vance_non_ref'], dash='dot'), name='Vance (Non-Refundable)'))
        fig.add_trace(go.Scatter(x=[earnings], y=[harris_ctc - baseline_ctc], mode='lines', line=dict(color=colors['harris']), name='Harris'))

    title = f'CTC Impact Comparison for {"Married" if filing_status == "married" else "Single"} Household'
    fig.update_layout(
        title=title,
        xaxis_title="Earnings",
        yaxis_title="CTC Impact (Reformed - Baseline)",
        xaxis=dict(tickformat='$,.0f', range=[0, MAX_INCOME]),
        yaxis=dict(tickformat='$,.0f'),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.01
        ),
        height=600,
        width=800,
    )
    return fig

# Streamlit app
st.title("Child Tax Credit (CTC) Reform Comparison")

st.write("""
This app compares the impact of different Child Tax Credit (CTC) reform proposals.
""")

# User inputs
filing_status = "married" if st.checkbox("Married household") else "single"

num_children = st.number_input("Number of children", min_value=0, max_value=10, value=1)

child_ages = []
for i in range(num_children):
    age = st.number_input(f"Age of child {i+1}", min_value=0, max_value=16, value=5)
    child_ages.append(age)

earnings = st.number_input("Household earnings for 2025", min_value=0, max_value=1000000, value=50000, step=1000)

if st.button("Generate Graphs"):
    # Bar chart for specific earnings
    fig_bar = create_reform_comparison_graph(filing_status, child_ages, earnings)
    fig_bar = format_fig(fig_bar)
    st.plotly_chart(fig_bar)
    
    # Line graph for range of earnings
    fig_line = create_reform_comparison_line_graph(filing_status, child_ages)
    fig_line = format_fig(fig_line)
    st.plotly_chart(fig_line)

st.write("""
### Notes:
- The bar chart shows the impact of each reform proposal on the CTC at the specific earnings entered.
- The line graph shows how the impact on the CTC changes across a range of earnings for each reform proposal.
- Impact is calculated as: Reformed CTC Value ('ctc') - Baseline CTC Value ('ctc_value').
- A positive value indicates an increase in the CTC under the reform, while a negative value indicates a decrease.
- The simulation is for the tax year 2025.
- Children must be under 17 years old to be eligible for the Child Tax Credit.
- This simulation assumes no premium tax credit, no itemized deductions, no alternative minimum tax, no net investment income tax, and no earned income tax credit to improve performance.
""")