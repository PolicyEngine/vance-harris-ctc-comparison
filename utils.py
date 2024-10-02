from reforms import vance_non_refundable, harris, VANCE_AMOUNT
from policyengine_us import Simulation

import yaml

# Colors
LIGHT_RED = "#f78989"
BLACK = "#000000"
BLUE_95 = "#D8E6F3"
BLUE_98 = "#F7FAFD"
BLUE = "#2C6496"
BLUE_LIGHT = "#D8E6F3"
BLUE_PRESSED = "#17354F"
BLUE_PRIMARY = "#2C6496"
DARK_BLUE_HOVER = "#1d3e5e"
DARK_GRAY = "#616161"
DARK_RED = "#b50d0d"
GRAY = "#808080"
LIGHT_GRAY = "#D3D3D3"
GREEN = "#29d40f"
LIGHT_GRAY = "#F2F2F2"
MEDIUM_DARK_GRAY = "#D2D2D2"
MEDIUM_LIGHT_GRAY = "#BDBDBD"
TEAL_ACCENT = "#39C6C0"
TEAL_LIGHT = "#F7FDFC"
TEAL_PRESSED = "#227773"
WHITE = "#FFFFFF"


YEAR = "2025"
DEFAULT_AGE = 40
MAX_INCOME = 300_000


def create_situation(is_married, child_ages, earnings, add_axes=False):
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
            }
        },
        "households": {
            "household": {"members": ["adult"], "state_name": {YEAR: "TX"}}
        },
    }
    if add_axes:
        situation["people"]["adult"]["axes"] = {YEAR: 0}
        if is_married:
            situation["people"]["spouse"]["axes"] = {YEAR: 0}
        for i, age in enumerate(child_ages):
            situation["people"][f"child_{i}"]["axes"] = {YEAR: 0}

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


def calculate_ctc(situation, reform=None, vary_earnings=False):
    if reform is "baseline":
        return Simulation(situation=situation).calculate("ctc_value", YEAR)[0]
    elif reform is "vance_refundable":
        # Calculate the number of children
        num_children = sum(
            1
            for person in situation["people"].values()
            if person.get("age", {}).get(YEAR, 100) < 17
        )
        return VANCE_AMOUNT * num_children
    elif reform is "vance_non_refundable":
        return Simulation(
            situation=situation, reform=vance_non_refundable
        ).calculate("ctc_value", YEAR)[0]
    elif reform is "harris":
        return Simulation(situation=situation, reform=harris).calculate(
            "refundable_ctc", YEAR
        )[0]
    else:
        raise ValueError("Unknown reform")
