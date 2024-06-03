import tempfile
import pytest
import config


@pytest.fixture()
def create_temp_molecule_database():
    temp_dict = tempfile.mkdtemp()
    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=temp_dict, suffix=".db")
    db = temp_file.name
    config.DB_PATH = db
    return db


