from utils import GRAY, BLUE, LIGHT_RED, LIGHTER_RED

REFORMS = [
    ("baseline", "Baseline"),
    ("harris", "Harris-Walz plan"),
    (
        "vance_non_refundable",
        "Vance suggestion<br>(non-refundable possibility)",
    ),
    ("vance_refundable", "Vance suggestion<br>(refundable possibility)"),
]

COLOR_MAP = {
    "Baseline": GRAY,
    "Harris-Walz plan": BLUE,
    "Vance suggestion<br>(refundable possibility)": LIGHT_RED,
    "Vance suggestion<br>(non-refundable possibility)": LIGHTER_RED,
}

APP_TITLE = "Child Tax Credit Calculator"

BASELINE_DESCRIPTION = """
## Current Child Tax Credit
The current Child Tax Credit provides up to $2,000 per qualifying child, phasing in and out with income. 
Enter your expected 2025 information below to see how much you'll be eligible for.

[Learn more about the current Child Tax Credit](https://policyengine.org/us/research/the-child-tax-credit-in-2023)
"""

REFORMS_DESCRIPTION = """
Members of the Democratic and Republican presidential tickets have indicated interest in expanding the Child Tax Credit:

- **Harris-Walz CTC plan**: The [Harris-Walz economic plan](https://kamalaharris.com/wp-content/uploads/2024/09/Policy_Book_Economic-Opportunity.pdf#page=11) calls for restoring the 2021 expansion that made it fully refundable and more generous, and adding a $2,400 "baby bonus".
  [Read our full report on the Harris-Walz CTC proposal.](https://policyengine.org/us/research/harris-ctc)

- **Vance CTC suggestion**: In an [August 2024 interview](https://www.youtube.com/watch?v=pK1V2q05Zi8), Senator and Vice Presidential nominee JD Vance suggested expanding the CTC to $5,000. Vance did not specify whether it was refundable, so we modeled both refundable and non-refundable scenarios. [Donald Trump's platform](https://rncplatform.donaldjtrump.com/?_gl=1*s9hec5*_gcl_au*MTE5NjQwNTg0MC4xNzI3ODgwOTQw&_ga=2.140186549.721558943.1727880940-379257754.1727880940) calls for making permanent the 2017 Tax Cuts and Jobs Act, including its Child Tax Credit expansion, but does not mention Vance's suggestion.
  [Read our full report on JD Vance's suggested CTC expansion.](https://policyengine.org/us/research/vance-ctc)

The graph below shows how these reforms would affect your Child Tax Credit:
"""

NOTES = """
### Assumptions:
- All earnings are from the tax filer's wages, salaries, and tips in 2025.
- The filer has no other taxable income.
- The filer takes the standard deduction.
- Married couples file jointly.
- Senator JD Vance's suggestion has the same age limit as the current CTC.
- Uses the policyengine-us Python package.
"""
