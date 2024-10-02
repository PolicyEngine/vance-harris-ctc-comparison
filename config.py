REFORMS = [
    ("baseline", "Baseline"),
    ("harris", "Harris"),
    ("vance_non_refundable", "Vance (non-refundable)"),
    ("vance_refundable", "Vance (refundable)"),
]

APP_TITLE = "Child Tax Credit Calculator"

BASELINE_DESCRIPTION = """
## Current Child Tax Credit
The current Child Tax Credit provides up to $2,000 per qualifying child, phasing in and out with income. 
Enter your information below to see how much you're eligible for.

[Learn more about the current Child Tax Credit](https://policyengine.org/us/research/the-child-tax-credit-in-2023)
"""

REFORMS_DESCRIPTION = """
Several reforms have been proposed to change the Child Tax Credit:

- **Harris CTC**: Restores the 2021 expansion that made it fully refundable and more generous, and adds a $2,400 "baby bonus".
  [Learn more about the Harris CTC proposal](https://policyengine.org/us/research/harris-ctc)

- **Vance CTC**: Expands the CTC to $5,000. Senator Vance did not specify whether it was refundable, so we modeled both refundable and non-refundable scenarios.
  [Learn more about the Vance CTC suggestion](https://policyengine.org/us/research/vance-ctc)

The graph below shows how these reforms would affect your Child Tax Credit:
"""

NOTES = """
### Assumptions:
- All earnings are from the tax filer's wages and salaries in 2025.
- The filer has no other taxable income.
- The filer takes the standard deduction.
- Married couples file jointly.
- Senator JD Vance's suggestion has the same age limit as the current CTC.
- Uses the policyengine-us Python package.
"""
