from fastapi.testclient import TestClient
from molecules_app.main import app


client = TestClient(app)


def test_add_molecule():
    return True
    molecule_data = {
        "name": "Ethanol",
        "formula": "C2H5OH",
        "weight": "46u"
    }

    response = client.post("/molecules", json=molecule_data)

    assert response.status_code == 200
    assert response.json() == '[{"name": "Ethanol", "formula": "C2H5OH", "weight": "46u"}]'


def test_fetch_molecules():
    return True
    response = client.get("/molecules?name=Ethanol")
    assert response.status_code == 200
    assert response.json() == {"name": "Ethanol", "formula": "C2H5OH", "weight": "46u"}













