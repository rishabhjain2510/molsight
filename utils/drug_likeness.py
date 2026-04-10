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


def get_descriptor_status(descriptors):
    def _tier(value, good_max, borderline_max):
        if value <= good_max:
            return "good", "Optimal"
        if value <= borderline_max:
            return "borderline", "Borderline"
        return "bad", "Too high"

    mw_s,  mw_m  = _tier(descriptors["Molecular Weight"], 500, 600)
    logp_s, logp_m = _tier(descriptors["LogP"], 5, 6)
    hbd_s,  hbd_m  = _tier(descriptors["H-Bond Donors"], 5, 7)
    hba_s,  hba_m  = _tier(descriptors["H-Bond Acceptors"], 10, 12)
    tpsa_s, tpsa_m = _tier(descriptors["TPSA"], 140, 160)
    rb_s,   rb_m   = _tier(descriptors["Rotatable Bonds"], 10, 15)

    return {
        "Molecular Weight":  {"status": mw_s,   "message": mw_m},
        "LogP":              {"status": logp_s,  "message": logp_m},
        "H-Bond Donors":     {"status": hbd_s,   "message": hbd_m},
        "H-Bond Acceptors":  {"status": hba_s,   "message": hba_m},
        "TPSA":              {"status": tpsa_s,  "message": tpsa_m},
        "Rotatable Bonds":   {"status": rb_s,    "message": rb_m},
    }


def generate_interpretation(descriptors, lipinski, bio_score):
    if bio_score > 0.75:
        verdict = "Excellent drug-likeness"
    elif bio_score >= 0.6:
        verdict = "Good drug-likeness"
    elif bio_score >= 0.4:
        verdict = "Moderate drug-likeness"
    else:
        verdict = "Poor drug-likeness"

    sentences = [f"This molecule shows {verdict.lower()}."]

    if lipinski["violations"] == 0:
        sentences.append("No Lipinski violations were observed.")
    else:
        sentences.append(f"There are {lipinski['violations']} Lipinski rule violation{'s' if lipinski['violations'] != 1 else ''}.")

    if descriptors["LogP"] > 5:
        sentences.append("High LogP may reduce solubility.")
    if descriptors["TPSA"] > 140:
        sentences.append("High TPSA may reduce membrane permeability.")
    if descriptors["Molecular Weight"] > 500:
        sentences.append("High molecular weight may reduce absorption.")

    return {"verdict": verdict, "summary": " ".join(sentences)}


def bioavailability_score(lipinski_result, descriptors):
    score = 1.0
    score -= lipinski_result["violations"] * 0.15
    if descriptors["LogP"] > 5:
        score -= 0.1
    if descriptors["TPSA"] > 140:
        score -= 0.1
    if descriptors["Molecular Weight"] > 500:
        score -= 0.1
    return round(max(0.0, min(1.0, score)), 2)
