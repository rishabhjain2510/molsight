import base64
from io import BytesIO
from rdkit import Chem
from rdkit.Chem import Draw


def smiles_to_base64_image(smiles, size=(300, 300)):
    """
    Convert a SMILES string to a base64-encoded PNG image.
    Returns a data URI string suitable for an <img src="..."> tag,
    or None if the SMILES is invalid.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    img = Draw.MolToImage(mol, size=size)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
