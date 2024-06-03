from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add_molecule(create_temp_molecule_database):
    molecule_data = {
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }

    response = client.post(f"/molecule", json=molecule_data)

    assert response.status_code == 200
    assert response.json() == {"name": "Ethanol", "formula": "C2H5OH", "weight": "46u"}


def test_add_molecules(create_temp_molecule_database):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }, {
        "name": "Water",
        "formula": "H2O",
        "weight": "18u"
    }]

    response = client.post(f"/molecule", json=molecule_data)

    assert response.status_code == 200
    assert response.json() == [{'formula': 'C2H5OH', 'name': 'Ethanol', 'weight': '46u'},
                               {'formula': 'H2O', 'name': 'Water', 'weight': '18u'}]


def test_fetch_molecule(create_temp_molecule_database):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }, {
        "name": "Water",
        "formula": "H2O",
        "weight": "18u"
    }]

    response = client.post(f"/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get(f"/molecule?name=Ethanol")
    assert response.status_code == 200
    assert response.json() == [['Ethanol', 'C2H5OH', '46u']]


def test_fetch_molecule_with_no_name(create_temp_molecule_database):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    response = client.post(f"/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get(f"/molecule")
    assert response.status_code == 200
    assert response.json() == "No query name"


def test_fetch_molecule_with_no_matching_molecule(create_temp_molecule_database):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    response = client.post(f"/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get(f"/molecule?name=Water")

    assert response.status_code == 200
    assert response.json() == "Name not found"


def test_find_molecules_with_H_element(create_temp_molecule_database):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    response = client.post(f"/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get(f"/molecules?element=H")

    assert response.status_code == 200
    assert response.json() == ['Ethanol']


def test_find_molecules_with_O_element(create_temp_molecule_database):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    response = client.post(f"/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get(f"/molecules?element=O")

    assert response.status_code == 200
    assert response.json() == ['Ethanol']


def test_find_molecules_with_no_matches(create_temp_molecule_database):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    response = client.post(f"/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get(f"/molecules?element=A")

    assert response.status_code == 200
    assert response.json() == 'Name not found'


def test_find_molecules_with_no_query(create_temp_molecule_database):
    molecule_data = [{
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }]
    response = client.post(f"/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get(f"/molecules")

    assert response.status_code == 200
    assert response.json() == "No query element"
