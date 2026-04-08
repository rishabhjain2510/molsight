def check_lipinski(descriptors):
    mw = descriptors["Molecular Weight"]
    logp = descriptors["LogP"]
    hbd = descriptors["H-Bond Donors"]
    hba = descriptors["H-Bond Acceptors"]

    rules = {
        "Molecular Weight <= 500": mw <= 500,
        "LogP <= 5": logp <= 5,
        "H-Bond Donors <= 5": hbd <= 5,
        "H-Bond Acceptors <= 10": hba <= 10,
    }

    violations = sum(1 for passed in rules.values() if not passed)

    if violations == 0:
        interpretation = (
            "This molecule satisfies all four Lipinski criteria, suggesting it may have "
            "favorable oral bioavailability. It is consistent with known orally active drugs."
        )
    elif violations == 1:
        interpretation = (
            "This molecule has one Lipinski violation. Oral bioavailability may still be "
            "achievable, but the property in question warrants further investigation. "
            "Some approved drugs exceed a single criterion."
        )
    else:
        interpretation = (
            f"This molecule has {violations} Lipinski violations, which is associated with "
            "reduced likelihood of good oral bioavailability. It may still have therapeutic "
            "value via non-oral routes, but significant optimization is typically required."
        )

    return {
        "rules": rules,
        "violations": violations,
        "drug_like": violations == 0,
        "interpretation": interpretation,
    }
