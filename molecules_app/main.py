from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

import config
from tables.molecule import Base, MoleculeInDB

app = FastAPI()


class Molecule(BaseModel):
    id: int | None = None
    name: str
    formula: str
    weight_in_units: float

    @staticmethod
    def from_molecule_in_db(molecule_in_db: MoleculeInDB):
        molecule = Molecule(id=molecule_in_db.id, name=molecule_in_db.name, formula=molecule_in_db.formula,
                            weight_in_units=molecule_in_db.weight_in_units)
        return molecule

    def to_molecule_in_db(self):
        molecule = MoleculeInDB(id=self.id, name=self.name, formula=self.formula,
                                weight_in_units=self.weight_in_units)
        return molecule


async def get_db():
    engine = create_engine(config.CONNECTION_STRING, echo=True)
    db = Session(engine)
    Base.metadata.create_all(engine)
    try:
        yield db
    finally:
        db.close()


@app.post("/molecule")
async def add_molecule(molecule: Molecule | list[Molecule], db=Depends(get_db)):
    if isinstance(molecule, list):
        for mol in molecule:
            mol = mol.to_molecule_in_db()
            db.add(mol)
    else:
        molecule = molecule.to_molecule_in_db()
        db.add(molecule)
    db.commit()
    return


@app.get("/molecule")
async def fetch_molecules(name: str, db=Depends(get_db)):
    result = db.scalars(select(MoleculeInDB).where(MoleculeInDB.name == name)).first()
    if not result:
        raise HTTPException(status_code=400, detail="Name not found")
    result = Molecule.from_molecule_in_db(result)
    return result


@app.get("/molecules")
async def find_molecules(element: str, db=Depends(get_db)):
    result = db.execute(select(MoleculeInDB.name, MoleculeInDB.formula))
    selected = []
    for mol in result:
        if element.upper() in mol.formula:
            selected.append(mol.name)
    if not selected:
        raise HTTPException(status_code=400, detail="Name not found")
    else:
        return selected


@app.delete("/molecules")
async def delete_molecules(db=Depends(get_db)):
    molecules = db.query(MoleculeInDB).all()
    for mol in molecules:
        db.delete(mol)
    db.commit()
