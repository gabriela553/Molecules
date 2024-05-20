import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Molecule(BaseModel):
    name: str
    formula: str
    weight: str


@app.post("/molecules")
async def add_molecule(molecule: Molecule | list[Molecule], file_path):
    with open(file_path, "r") as file:
        content = json.load(file)
        if isinstance(molecule, list):
            for mol in molecule:
                content.append(mol.model_dump())
        else:
            content.append(molecule.model_dump())
    content = json.dumps(content)
    with open(file_path, "w") as file:
        file.write(content)
    return content


@app.get("/molecules")
async def fetch_molecules(file_path_add, name: str | None = None) -> Molecule | list[Molecule]:
    with open(file_path_add, "r") as file:
        content = json.load(file)
        if name:
            for mol in content:
                if mol["name"] == name:
                    return Molecule(**mol)
        else:
            return [Molecule(**mol) for mol in content]
