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
MAX_INCOME = 300000

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
    
    if reform in [vance_ref, reform_harris]:
        return simulation.calculate("refundable_ctc", YEAR)[0]
    elif reform is vance_non_ref or reform is None:
        return simulation.calculate("ctc_value", YEAR)[0]
    else:
        raise ValueError("Unknown reform")

def create_reform_comparison_graph(filing_status, child_ages, earnings):
    colors = {
        "baseline": "#D3D3D3",    # Light grey for baseline
        "vance_ref": "#18375f",   # Dark blue
        "vance_non_ref": "#2976fe", # Light blue
        "harris": "#4682B4",      # Steel blue for Harris
    }
    
    situation = create_situation(filing_status, child_ages, earnings)
    baseline_ctc = calculate_ctc(situation)
    vance_ref_ctc = calculate_ctc(situation, vance_ref)
    vance_non_ref_ctc = calculate_ctc(situation, vance_non_ref)
    harris_ctc = calculate_ctc(situation, reform_harris)
    
    reforms = ["Current Law", "Vance (Refundable)", "Vance (Non-Refundable)", "Harris"]
    ctc_values = [
        baseline_ctc,
        vance_ref_ctc,
        vance_non_ref_ctc,
        harris_ctc
    ]
    
    fig = go.Figure()
    
    # Add baseline bar
    fig.add_trace(go.Bar(
        x=[reforms[0]],
        y=[ctc_values[0]],
        name="Current Law",
        marker_color=colors["baseline"]
    ))
    
    # Add impact bars
    for reform, value, color in zip(reforms[1:], ctc_values[1:], [colors["vance_ref"], colors["vance_non_ref"], colors["harris"]]):
        fig.add_trace(go.Bar(
            x=[reform],
            y=[value],
            name=reform,
            marker_color=color
        ))
    
    fig.update_layout(
        title=f'CTC value Comparison',
        xaxis_title="Reform",
        yaxis_title="CTC Value / Impact",
        yaxis=dict(tickformat='$,.0f'),
        legend_title="Reforms",
        barmode='group',
        height=500,
        width=800,
    )
    
    return fig

def create_reform_comparison_line_graph(filing_status, child_ages):
    colors = {
        "vance_ref": "#18375f",   # Dark blue
        "vance_non_ref": "#2976fe", # Light blue
        "harris": "#4682B4",      # Steel blue for Harris
    }
    
    def create_situation(filing_status, child_ages):
        situation = {
            "people": {
                "adult": {
                    "age": {YEAR: DEFAULT_AGE},
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

    situation = create_situation(filing_status, child_ages)
    
    fig = go.Figure()
    
    x = np.linspace(0, MAX_INCOME, 501)
    
    # Calculate baseline values
    baseline_simulation = Simulation(situation=situation)
    baseline_household_net_income = baseline_simulation.calculate("household_net_income", YEAR)


    reforms = {
        "vance_ref": vance_ref,
        "vance_non_ref": vance_non_ref,
        "harris": reform_harris
    }

    for reform_name, reform in reforms.items():
        simulation = Simulation(situation=situation, reform=reform)
        
        reformed_household_net_income = simulation.calculate("household_net_income", YEAR)
        
        net_income_impact = reformed_household_net_income - baseline_household_net_income

        name = reform_name.replace("_", " ").title()
        fig.add_trace(go.Scatter(x=x, y=net_income_impact, mode='lines', line=dict(color=colors[reform_name]), name=name))

    title = f'CTC Reform total net income Impact'
    fig.update_layout(
        title=title,
        xaxis_title="Earnings",
        yaxis_title="Net Income Impact (Reform - Baseline)",
        xaxis=dict(tickformat='$,.0f', range=[0, MAX_INCOME]),
        yaxis=dict(tickformat='$,.0f', zeroline=True, zerolinewidth=2, zerolinecolor='black'),
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
st.title("Harris vs Vance Child Tax Credit (CTC) Reform Comparison")

# User inputs
filing_status = "married" if st.checkbox("Married household") else "single"

num_children = st.number_input("Number of children", min_value=0, max_value=10, value=1)

child_ages = []
for i in range(num_children):
    age = st.number_input(f"Age of child {i+1}", min_value=0, max_value=16, value=5)
    child_ages.append(age)

earnings = st.number_input("Household wages and salaries in 2025", min_value=0, max_value=1000000, value=50000, step=1000)

if st.button("Generate Comparison"):
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
- All earnings are from the tax filer's wages and salaries.
- The filer has no other taxable income.
- The filer takes the standard deduction.
- Married couples file jointly.
""")