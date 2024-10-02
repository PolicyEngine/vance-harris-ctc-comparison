from policyengine_core.reforms import Reform

import yaml

VANCE_AMOUNT = 5_000

# Define the reforms.
# We calculate the Vance refundable reform as $5,000 per child
# without the reform model itself.
# We present it here for the sake of completeness.
vance_refundable = Reform.from_dict(
    {
        "gov.irs.credits.ctc.amount.base[0].amount": {
            "2024-01-01.2100-12-31": VANCE_AMOUNT
        },
        "gov.irs.credits.ctc.phase_out.amount": {"2024-01-01.2100-12-31": 0},
        "gov.irs.credits.ctc.refundable.fully_refundable": {
            "2024-01-01.2100-12-31": True
        },
    },
    country_id="us",
)

vance_non_refundable = Reform.from_dict(
    {
        "gov.irs.credits.ctc.amount.base[0].amount": {
            "2024-01-01.2100-12-31": VANCE_AMOUNT
        },
        "gov.irs.credits.ctc.phase_out.amount": {"2024-01-01.2100-12-31": 0},
    },
    country_id="us",
)

harris = Reform.from_dict(
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
