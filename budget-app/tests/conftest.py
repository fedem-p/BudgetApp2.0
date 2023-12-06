"""Fixtures for the test module."""
import os
import sys

import pytest

# Get the directory containing your module
module_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sys.path.append('../')
sys.path.insert(0, module_directory)
# pylint: disable=C0116, W0621
from core.data_manager import DATA_CSV, METADATA_JSON  # pylint: disable=C0413,E0401

TEST_FOLDER_PATH = "/tmp/tmp_empty_dir/"


def clean_data(folder_path):
    """Clean all data inside a folder.

    Args:
        folder_path (str): path to the folder.
    """
    csv_file_path = os.path.join(folder_path, DATA_CSV)
    json_file_path = os.path.join(folder_path, METADATA_JSON)

    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)


@pytest.fixture
def create_empty_folder():
    """Fixture to create an empty folder.

    Yields:
        str: folder path.
    """
    empty_folder = TEST_FOLDER_PATH
    os.mkdir(empty_folder)
    yield empty_folder
    clean_data(folder_path=empty_folder)
    os.rmdir(empty_folder)


@pytest.fixture
def create_full_folder(create_empty_folder):
    """Fixture to create a folder with data files inside..

    Yields:
        str: folder path.
    """
    folder = create_empty_folder
    csv_file_path = os.path.join(folder, DATA_CSV)
    json_file_path = os.path.join(folder, METADATA_JSON)

    with open(csv_file_path, "w", encoding="utf8"):
        pass
    with open(json_file_path, "w", encoding="utf8"):
        pass

    yield folder
    clean_data(folder_path=folder)
