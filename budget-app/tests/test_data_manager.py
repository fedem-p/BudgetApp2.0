import sys

import pytest

# Get the directory containing your module
module_directory = "/home/fpuppo/workspace/budget-app/budget-app/core"

# Append the module directory to sys.path
sys.path.append(module_directory)

import os

from data_manager import EXAMPLE_DATA, EXAMPLE_METADATA, DataManager

TEST_FOLDER_PATH = "/tmp/tmp_empty_dir/"


def clean_data(folder_path):
    csv_file_path = os.path.join(folder_path, "data.csv")
    json_file_path = os.path.join(folder_path, "metadata.json")

    if os.path.exists(json_file_path):
        os.remove(json_file_path)
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)


@pytest.fixture
def create_empty_folder():
    empty_folder = TEST_FOLDER_PATH
    os.mkdir(empty_folder)
    yield empty_folder
    clean_data(folder_path=empty_folder)
    os.rmdir(empty_folder)


@pytest.fixture
def create_full_folder(create_empty_folder):
    folder = create_empty_folder
    csv_file_path = os.path.join(folder, "data.csv")
    json_file_path = os.path.join(folder, "metadata.json")

    with open(csv_file_path, "w"):
        pass
    with open(json_file_path, "w"):
        pass

    yield folder
    clean_data(folder_path=folder)


def test_is_empty_data_folder_true(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)

    assert new_manager.is_empty_data_folder() == True


def test_is_empty_data_folder_false(create_full_folder):
    new_manager = DataManager(data_folder=create_full_folder)

    assert new_manager.is_empty_data_folder() == False


def test_create_data_file(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)

    new_manager.create_data_file()

    assert sorted(["metadata.json", "data.csv"]) == sorted(
        os.listdir(create_empty_folder)
    )


@pytest.mark.skip
# TODO fix test
def test_load_csv(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)

    new_manager.create_data_file()

    csv_data = new_manager.load_csv()

    print(csv_data)

    for i in range(1, 7):
        for name, element in zip(EXAMPLE_DATA[0], EXAMPLE_DATA[i]):
            assert element in csv_data[name]


def test_load_metadata(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)

    new_manager.create_data_file()
    new_manager.load_metadata()
    json_data = new_manager.metadata

    for key, value in EXAMPLE_METADATA.items():
        assert json_data[key] == value


def test_initialize_data(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)

    new_manager.initialize_data()

    assert new_manager.accounts == EXAMPLE_METADATA["accounts"]
    assert new_manager.categories == EXAMPLE_METADATA["categories"]
    assert new_manager.sub_categories == EXAMPLE_METADATA["subcategories"]


# def test_load_transactions(create_empty_folder):
#     new_manager = DataManager(data_folder=create_empty_folder)

#     new_manager.create_data_file()

#     assert new_manager.is_empty_data_folder() == False
