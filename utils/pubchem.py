import requests
from urllib.parse import quote


def fetch_molecule_name(smiles):
    """Return the IUPAC name for a SMILES string via PubChem, or 'Not available' on any failure."""
    try:
        url = (
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/"
            f"{quote(smiles, safe='')}/property/IUPACName/JSON"
        )
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()["PropertyTable"]["Properties"][0]["IUPACName"]
    except Exception:
        return "Not available"
