import json
from pathlib import Path
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Molecule(BaseModel):
    name: str
    formula: str
    weight: str


db: List[Molecule] = [
    Molecule(name="Acetone", formula="CH3COCH3", weight="58u"),
    Molecule(name="Water", formula="H20", weight="18u")
]

file_path = "C:\\Users\\gabi0\\Desktop\\chemical.txt"


@app.post("/molecules")
async def add_molecule(molecule: Molecule):
    p = Path(file_path)
    if not p.exists():
        with p.open('w') as file:
            content = json.dumps([])
            file.write(content)
    with open(file_path, "r") as file:
        content = json.load(file)
        content.append(molecule.model_dump())
    content = json.dumps(content)
    with open(file_path, "w") as file:
        file.write(content)
    return content


@app.get("/molecules")
async def fetch_molecules(name: str | None = None):
    if name:
        for mol in db:
            if name == mol.name:
                return mol
    else:
        return db


# DB for testing
'''
db: List[Molecule] = [
    {"name":"Ethanol","formula":"C2H5OH","weight":"46u"}
    {"name":"Acetic acid","formula":"CH3COOH","weight":"60u"}
]
'''
