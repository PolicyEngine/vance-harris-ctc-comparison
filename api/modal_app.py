import modal

app = modal.App("vance-harris-ctc")

image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "policyengine-us==1.95.0",
    "fastapi[standard]",
)


VANCE_AMOUNT = 5_000
YEAR = "2025"
DEFAULT_AGE = 40


def create_situation(is_married: bool, child_ages: list[int], earnings: int):
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
                "premium_tax_credit": {YEAR: 0},
                "tax_unit_itemizes": {YEAR: False},
                "taxable_income_deductions_if_itemizing": {YEAR: 0},
                "alternative_minimum_tax": {YEAR: 0},
                "net_investment_income_tax": {YEAR: 0},
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
            situation[unit][list(situation[unit].keys())[0]]["members"].append(
                child_id
            )

    if is_married:
        situation["people"]["spouse"] = {"age": {YEAR: DEFAULT_AGE}}
        for unit in ["families", "marital_units", "tax_units", "households"]:
            situation[unit][list(situation[unit].keys())[0]]["members"].append(
                "spouse"
            )

    return situation


@app.function(image=image, timeout=300)
@modal.fastapi_endpoint(method="GET")
def calculate(
    is_married: bool = False,
    num_children: int = 1,
    child_ages: str = "5",
    earnings: int = 50000,
):
    from policyengine_us import Simulation
    from policyengine_core.reforms import Reform

    ages = [int(a) for a in child_ages.split(",") if a.strip()]
    situation = create_situation(is_married, ages, earnings)

    # Baseline
    baseline = float(
        Simulation(situation=situation).calculate("ctc_value", YEAR)[0]
    )

    # Harris reform
    harris_reform = Reform.from_dict(
        {
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
            },
        },
        country_id="us",
    )
    harris = float(
        Simulation(situation=situation, reform=harris_reform).calculate(
            "refundable_ctc", YEAR
        )[0]
    )

    # Vance non-refundable
    vance_nr_reform = Reform.from_dict(
        {
            "gov.irs.credits.ctc.amount.base[0].amount": {
                "2024-01-01.2100-12-31": VANCE_AMOUNT
            },
            "gov.irs.credits.ctc.phase_out.amount": {
                "2024-01-01.2100-12-31": 0
            },
        },
        country_id="us",
    )
    vance_non_refundable = float(
        Simulation(situation=situation, reform=vance_nr_reform).calculate(
            "ctc_value", YEAR
        )[0]
    )

    # Vance refundable = simply $5,000 * qualifying children
    num_qualifying = sum(1 for a in ages if a < 17)
    vance_refundable = float(VANCE_AMOUNT * num_qualifying)

    return {
        "baseline": baseline,
        "harris": harris,
        "vance_non_refundable": vance_non_refundable,
        "vance_refundable": vance_refundable,
        "year": YEAR,
    }
