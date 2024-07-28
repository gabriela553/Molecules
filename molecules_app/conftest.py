
'''
import tempfile

import pytest
from sqlalchemy import create_engine

import config
from main import Base

@pytest.fixture()
def create_temp_molecule_database():
    temp_dict = tempfile.mkdtemp()
    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=temp_dict, suffix=".db")
    db = temp_file.name
    config.DATABASE_PATH = db
    engine = create_engine(config.CONNECTION_STRING, echo=True)
    Base.metadata.create_all(engine)
    return db
'''

