from fastapi.testclient import TestClient

from molecules_app.main import app

client = TestClient(app)


def test_add_molecule():
    molecule_data = {"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46}

    response = client.post("/molecule", json=molecule_data)

    assert response.status_code == 200
    client.delete("/molecules")


def test_add_molecules():
    molecule_data = [
        {"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46},
        {"name": "Water", "formula": "H2O", "weight_in_units": 18},
    ]

    response = client.post("/molecule", json=molecule_data)

    assert response.status_code == 200
    client.delete("/molecules")


def test_fetch_molecule():
    molecule_data = [
        {"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46},
        {"name": "Water", "formula": "H2O", "weight_in_units": 18},
    ]

    response = client.post("/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get("/molecule?name=Ethanol")
    result = response.json()
    assert response.status_code == 200
    assert result["name"] == "Ethanol"
    assert result["formula"] == "C2H5OH"
    assert result["weight_in_units"] == 46.0
    client.delete("/molecules")


def test_fetch_molecule_with_no_name():
    molecule_data = [{"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46}]
    response = client.post("/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get("/molecule")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": None,
                "loc": ["query", "name"],
                "msg": "Field required",
                "type": "missing",
            }
        ]
    }
    client.delete("/molecules")


def test_fetch_molecule_with_no_matching_molecule():
    molecule_data = [{"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46}]
    response = client.post("/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get("/molecule?name=Water")

    assert response.status_code == 400
    assert response.json() == {"detail": "Name not found"}
    client.delete("/molecules")


def test_find_molecules_with_H_element():
    molecule_data = [{"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46}]
    response = client.post("/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get("/molecules?element=H")

    assert response.status_code == 200
    assert response.json() == ["Ethanol"]
    client.delete("/molecules")


def test_find_molecules_with_O_element():
    molecule_data = [{"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46}]
    response = client.post("/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get("/molecules?element=O")

    assert response.status_code == 200
    assert response.json() == ["Ethanol"]
    client.delete("/molecules")


def test_find_molecules_with_no_matches():
    molecule_data = [{"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46}]
    response = client.post("/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get("/molecules?element=A")

    assert response.status_code == 400
    assert response.json() == {"detail": "Name not found"}
    client.delete("/molecules")


def test_find_molecules_with_no_query():
    molecule_data = [{"name": "Ethanol", "formula": "C2H5OH", "weight_in_units": 46}]
    response = client.post("/molecule", json=molecule_data)
    assert response.status_code == 200

    response = client.get("/molecules")

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "element"],
                "msg": "Field required",
                "input": None,
            }
        ]
    }
    client.delete("/molecules")
