import json
from config import create_molecule_file
from fastapi.testclient import TestClient
from molecules_app.main import app

client = TestClient(app)


def test_add_molecule(create_molecule_file):
    molecule_data = {
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }

    response = client.post(f"/molecules?file_path={create_molecule_file}", json=molecule_data)

    assert response.status_code == 200
    assert response.json() == '[{"name": "Ethanol", "formula": "C2H5OH", "weight": "46u"}]'


def test_add_molecules(create_molecule_file):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }, {
        "name": "Water",
        "formula": "H2O",
        "weight": "18u"
    }]

    response = client.post(f"/molecules?file_path={create_molecule_file}", json=molecule_data)

    assert response.status_code == 200
    assert response.json() == ('[{"name": "Ethanol", "formula": "C2H5OH", "weight": "46u"}, {"name": "Water", '
                               '"formula": "H2O", "weight": "18u"}]')


def test_fetch_molecule(create_molecule_file):
    file_path_add = create_molecule_file
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    with open(file_path_add, 'w') as file:
        content = json.dumps(molecule_data)
        file.write(content)

    response = client.get(f"/molecules?file_path_add={file_path_add}&name=Ethanol")

    assert response.status_code == 200
    assert response.json() == {"name": "Ethanol", "formula": "C2H5OH", "weight": "46u"}


def test_fetch_molecules(create_molecule_file):
    file_path_add = create_molecule_file
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }, {
        "name": "Water",
        "formula": "H2O",
        "weight": "18u"
    }]
    with open(file_path_add, 'w') as file:
        content = json.dumps(molecule_data)
        file.write(content)

    response = client.get(f"/molecules?file_path_add={file_path_add}&name=Water")

    assert response.status_code == 200
    assert response.json() == {'formula': 'H2O', 'name': 'Water', 'weight': '18u'}


def test_fetch_molecule_with_no_name(create_molecule_file):
    file_path_add = create_molecule_file
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    with open(file_path_add, 'w') as file:
        content = json.dumps(molecule_data)
        file.write(content)

    response = client.get(f"/molecules?file_path_add={file_path_add}")

    assert response.status_code == 200
    assert response.json() == [{"name": "Ethanol", "formula": "C2H5OH", "weight": "46u"}]


def test_fetch_molecule_with_no_file_path(create_molecule_file):
    file_path_add = create_molecule_file
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    with open(file_path_add, 'w') as file:
        content = json.dumps(molecule_data)
        file.write(content)

    response = client.get(f"/molecules?name=Water")

    assert response.status_code == 422
