import tempfile
import pytest
import json


@pytest.fixture()
def create_molecule_file():
    temp_dict = tempfile.mkdtemp()
    temp_file = tempfile.NamedTemporaryFile(delete=False, dir=temp_dict)
    file_path = temp_file.name
    with open(file_path, 'w') as file:
        content = json.dumps([])
        file.write(content)
    temp_file.close()
    return file_path
