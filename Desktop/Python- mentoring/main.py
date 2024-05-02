import json
import os
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

file_path = "C:\\Users\\gabi0\\Desktop\\chemical.json"


# Do not know how to save this in json format


@app.post("/molecules")
async def add_molecule(molecule: Molecule):
    db.append(molecule)
    if os.path.getsize(file_path) == 0:
        with open(file_path, "w+") as file:
            # json.dumps(db, indent=2)
            file.write(f"{db}")
    else:
        with open(file_path, "a") as file:
            file.write(f"{molecule}")
            # json.dump(molecule, file)
    return


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
