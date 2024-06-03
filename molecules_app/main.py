import sqlite3
import config
from fastapi import Depends, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Molecule(BaseModel):
    name: str
    formula: str
    weight: str


async def get_db():
    db = sqlite3.connect(config.DB_PATH)
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE if not exists molecules (
            name string,
            formula string,
            weight string)
            
    ''')

    db.commit()
    return db


@app.post("/molecule")
async def add_molecule(molecule: Molecule | list[Molecule], db=Depends(get_db)):
    if isinstance(molecule, list):
        for mol in molecule:
            db.execute(f'''INSERT INTO molecules (name, formula, weight) VALUES ("{mol.name}", "{mol.formula}", 
            "{mol.weight}")''')
    else:
        db.execute(f'''INSERT INTO molecules (name, formula, weight) VALUES ("{molecule.name}", "{molecule.formula}", 
        "{molecule.weight}")''')
    db.commit()
    db.close()
    return molecule


@app.get("/molecule")
async def fetch_molecules(name: str | None = None, db=Depends(get_db)):
    if name:
        results = db.execute(f'''SELECT * FROM molecules WHERE name = "{name}" ''')
        results = results.fetchall()
        db.close()
        if results:
            return results
        else:
            return "Name not found"
    else:
        return "No query name"


@app.get("/molecules")
async def find_molecules(element: str | None = None, db=Depends(get_db)):
    if element:
        results = db.execute(f'''SELECT * FROM molecules''')
        results = results.fetchall()
        selected = []
        for mol in results:
            if element.upper() in str(mol[1]):
                selected.append(mol[0])
        db.close()
        if not selected:
            return "Name not found"
        else:
            return selected
    else:
        return "No query element"
