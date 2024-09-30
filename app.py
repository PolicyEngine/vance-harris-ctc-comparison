import streamlit as st
import numpy as np
import plotly.graph_objects as go
from policyengine_us import Simulation
from policyengine_core.reforms import Reform
from policyengine_core.charts import format_fig

# Define the reforms
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

def create_situation(filing_status, child_ages):
    situation = {
        "people": {
            "adult": {
                "age": {YEAR: DEFAULT_AGE},
            },
        },
        "families": {"family": {"members": ["adult"]}},
        "marital_units": {"marital_unit": {"members": ["adult"]}},
        "tax_units": {"tax_unit": {"members": ["adult"]}},
        "households": {
            "household": {"members": ["adult"], "state_name": {YEAR: "TX"}}
        },
        "axes": [[
            {
                "name": "employment_income",
                "min": 0,
                "max": MAX_INCOME,
                "count": 501,
                "period": YEAR,
            }
        ]]
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

def calculate_income(situation, reform=None):
    simulation = Simulation(situation=situation, reform=reform)
    return simulation.calculate("household_net_income", YEAR)

def create_reform_comparison_graph(filing_status, child_ages):
    colors = {
        "vance_ref": "#18375f",     # Dark blue
        "vance_non_ref": "#2976fe", # Light blue
        "harris": "#c5c5c5",        # Grey
    }
    
    x = np.linspace(0, MAX_INCOME, 501)
    fig = go.Figure()
    
    situation = create_situation(filing_status, child_ages)
    baseline = calculate_income(situation)
    vance_ref_result = calculate_income(situation, vance_ref)
    vance_non_ref_result = calculate_income(situation, vance_non_ref)
    harris_result = calculate_income(situation, reform_harris)
    
    fig.add_trace(go.Scatter(x=x, y=vance_ref_result - baseline, mode='lines', name='Vance (Refundable)', line=dict(color=colors['vance_ref'])))
    fig.add_trace(go.Scatter(x=x, y=vance_non_ref_result - baseline, mode='lines', name='Vance (Non-Refundable)', line=dict(color=colors['vance_non_ref'], dash='dot')))
    fig.add_trace(go.Scatter(x=x, y=harris_result - baseline, mode='lines', name='Harris', line=dict(color=colors['harris'])))

    title = f'Impact of CTC Reforms for {"Married" if filing_status == "married" else "Single"} Household'
    fig.update_layout(
        title=title,
        xaxis_title="Earnings",
        yaxis_title="Net Impact (Reformed - Baseline)",
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
This app compares the impact of different Child Tax Credit (CTC) reform proposals on household income.
""")

# User inputs
filing_status = "married" if st.checkbox("Married household") else "single"

num_children = st.number_input("Number of children", min_value=0, max_value=10, value=1)

child_ages = []
for i in range(num_children):
    age = st.number_input(f"Age of child {i+1}", min_value=0, max_value=5, value=5)
    child_ages.append(age)

if st.button("Generate Graph"):
    fig = create_reform_comparison_graph(filing_status, child_ages)
    fig = format_fig(fig)
    st.plotly_chart(fig)

st.write("""
### Notes:
- The graph shows the difference in household net income between each reform and the baseline (current law).
- A positive value indicates an increase in household income under the reform.
- The simulation is for the tax year 2025.
""")