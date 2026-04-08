from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from utils.pubchem import fetch_molecule_name

def calculate_descriptors(smiles):
    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None, None

    canonical_smiles = Chem.MolToSmiles(mol)

    descriptors = {
        "molecule_name": fetch_molecule_name(canonical_smiles),
        "Molecular Formula": rdMolDescriptors.CalcMolFormula(mol),
        "Molecular Weight": round(Descriptors.MolWt(mol), 2),
        "LogP": round(Descriptors.MolLogP(mol), 2),
        "H-Bond Donors": Descriptors.NumHDonors(mol),
        "H-Bond Acceptors": Descriptors.NumHAcceptors(mol),
        "TPSA": round(Descriptors.TPSA(mol), 2),
        "Rotatable Bonds": Descriptors.NumRotatableBonds(mol)
    }

    return descriptors, canonical_smiles