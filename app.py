import csv
import io
import os
from flask import Flask, render_template, request, Response
from utils.descriptor_calc import calculate_descriptors
from utils.drug_likeness import check_lipinski, bioavailability_score, generate_interpretation, get_descriptor_status
from utils.mol_image import smiles_to_base64_image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

def _analyse(smiles):
    """Run the full analysis pipeline for one SMILES. Returns a dict or None on invalid input."""
    result, canonical_smiles = calculate_descriptors(smiles)
    if result is None:
        return None
    lipinski = check_lipinski(result)
    bio_score = bioavailability_score(lipinski, result)
    return {
        "smiles":           smiles,
        "canonical_smiles": canonical_smiles,
        "data":             result,
        "lipinski":         lipinski,
        "mol_image":        smiles_to_base64_image(smiles),
        "bio_score":         bio_score,
        "interpretation":    generate_interpretation(result, lipinski, bio_score),
        "descriptor_status": get_descriptor_status(result),
    }


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    smiles = request.form.get("smiles")

    result, canonical_smiles = calculate_descriptors(smiles)

    if result is None:
        return render_template("index.html", error="Invalid SMILES string")

    lipinski = check_lipinski(result)
    mol_image = smiles_to_base64_image(smiles)
    bio_score = bioavailability_score(lipinski, result)
    interpretation = generate_interpretation(result, lipinski, bio_score)
    descriptor_status = get_descriptor_status(result)
    return render_template("result_rdkit.html", data=result, smiles=smiles, lipinski=lipinski, mol_image=mol_image, canonical_smiles=canonical_smiles, bio_score=bio_score, interpretation=interpretation, descriptor_status=descriptor_status)


@app.route("/export_csv", methods=["POST"])
def export_csv():
    smiles = request.form.get("smiles")

    result, canonical_smiles = calculate_descriptors(smiles)

    if result is None:
        return render_template("index.html", error="Invalid SMILES string")

    lipinski = check_lipinski(result)

    buf = io.StringIO()
    writer = csv.writer(buf)

    writer.writerow(["Field", "Value"])
    writer.writerow(["Input SMILES", smiles])
    writer.writerow(["Canonical SMILES", canonical_smiles])
    writer.writerow([])

    writer.writerow(["Descriptor", "Value"])
    for key, value in result.items():
        writer.writerow([key, value])
    writer.writerow([])

    writer.writerow(["Lipinski Rule", "Result"])
    for rule, passed in lipinski["rules"].items():
        writer.writerow([rule, "PASS" if passed else "FAIL"])
    writer.writerow(["Total Violations", f"{lipinski['violations']} / 4"])
    writer.writerow(["Drug-like", "Yes" if lipinski["drug_like"] else "No"])

    return Response(
        buf.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=molsight_results.csv"}
    )


@app.route("/compare", methods=["GET"])
def compare():
    return render_template("compare.html")


@app.route("/guide") 
def guide():
    return render_template("guide.html")


@app.route("/compare_result", methods=["POST"])
def compare_result():
    smiles1 = request.form.get("smiles1", "").strip()
    smiles2 = request.form.get("smiles2", "").strip()

    errors = {}
    if not smiles1:
        errors["smiles1"] = "Please enter a SMILES string for Molecule 1"
    if not smiles2:
        errors["smiles2"] = "Please enter a SMILES string for Molecule 2"

    if errors:
        return render_template("compare.html", errors=errors, smiles1=smiles1, smiles2=smiles2)

    mol1 = _analyse(smiles1)
    mol2 = _analyse(smiles2)

    if mol1 is None:
        errors["smiles1"] = "Invalid SMILES for Molecule 1"
    if mol2 is None:
        errors["smiles2"] = "Invalid SMILES for Molecule 2"

    if errors:
        return render_template("compare.html", errors=errors, smiles1=smiles1, smiles2=smiles2)

    return render_template("compare_result.html", mol1=mol1, mol2=mol2)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)