# MolSight

A Flask-based cheminformatics web app for molecular descriptor calculation and drug-likeness analysis.

## Features

- **Single Molecule Analysis** — input a SMILES string to calculate molecular descriptors and Lipinski Rule of Five compliance
- **2D Structure Visualisation** — RDKit-generated molecule images embedded inline
- **Molecular Descriptors** — Molecular Weight, LogP, H-Bond Donors/Acceptors, TPSA, Rotatable Bonds, Molecular Formula
- **IUPAC Name Lookup** — PubChem REST API integration
- **Canonical SMILES** — normalised via RDKit
- **Drug-likeness Verdict** — Lipinski Ro5 with per-rule pass/fail badges and interpretation
- **Molecule Comparison** — side-by-side analysis of two molecules with a unified descriptor table
- **CSV Export** — download full results including descriptors and Lipinski breakdown
- **Descriptor Guide** — reference page explaining each descriptor with thresholds and clinical context

## Tech Stack

- **Backend** — Python, Flask, RDKit
- **Frontend** — Jinja2 templates, Tailwind CSS (CDN), Newsreader + Manrope (Google Fonts)
- **Data** — PubChem REST API
- **Deployment** — Gunicorn, Render

## Project Structure

```
molfeature/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── static/
│   ├── css/
│       └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result_rdkit.html
│   ├── compare.html
│   ├── compare_result.html
│   └── guide.html
└── utils/
    ├── descriptor_calc.py
    ├── drug_likeness.py
    ├── mol_image.py
    └── pubchem.py
```

## Running Locally

```bash
conda activate molfeature
python app.py
```

The app runs at `http://localhost:5000` by default.

To enable debug mode locally:

```bash
FLASK_DEBUG=true python app.py
```

## Deployment (Render)

1. Push the repository to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repository
4. Render will automatically detect the `Procfile` and `requirements.txt`
5. No additional environment variables are required

The app is served by Gunicorn in production:

```
web: gunicorn app:app
```
