import os
import sys

import pytest

# Get the directory containing your module
module_directory = os.path.abspath("../core/")

# Append the module directory to sys.path
sys.path.append(module_directory)

import os

from data_manager import (
    DATA_CSV,
    EXAMPLE_DATA,
    EXAMPLE_METADATA,
    METADATA_JSON,
    DataManager,
    is_used,
    validate_input,
)

TEST_FOLDER_PATH = "/tmp/tmp_empty_dir/"


def clean_data(folder_path):
    csv_file_path = os.path.join(folder_path, DATA_CSV)
    json_file_path = os.path.join(folder_path, METADATA_JSON)

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
    csv_file_path = os.path.join(folder, DATA_CSV)
    json_file_path = os.path.join(folder, METADATA_JSON)

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

    assert sorted([METADATA_JSON, DATA_CSV]) == sorted(os.listdir(create_empty_folder))


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


def test_load_transactions(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)

    new_manager.create_data_file()

    new_manager.load_transactions()
    transactions = new_manager.transactions

    for idx, row_element in enumerate(transactions):
        for k, v in row_element.items():
            assert v == EXAMPLE_DATA[idx][k]


def test_get_account_balance_no_update(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)

    new_manager.create_data_file()

    new_manager.load_transactions()

    new_manager.balances = {"test": 20}

    assert new_manager.get_account_balance(account="test") == 20


def test_get_account_balance_update(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)

    new_manager.create_data_file()

    new_manager.load_transactions()

    assert new_manager.get_account_balance(account="N26") == round(34.5, 2)
    assert new_manager.get_account_balance(account="C24") == round(50.00, 2)
    assert new_manager.get_account_balance(account="Wallet") == round(15.98, 2)


@pytest.mark.parametrize(
    "item, item_list, item_type, mode, expected_exception, expected_message",
    [
        (
            2,
            [1, 2, 3],
            int,
            "add",
            ValueError,
            "Integrity Error: Item: 2 already exists!",
        ),
        (4, [1, 2, 3], int, "add", None, None),
        (2, [1, 2, 3], int, "remove", None, None),
        (4, [1, 2, 3], int, "remove", ValueError, "404 Error: Item: 4 not found!"),
        (
            2,
            [1, 2, 3],
            int,
            "invalid",
            ValueError,
            "Mode Error: Mode can only be 'add' or 'remove'!",
        ),
        (
            2,
            [1, 2, 3],
            str,
            "add",
            ValueError,
            "Type Error: 2 is not type <class 'str'>",
        ),
    ],
)
def test_validate_input(
    item, item_list, item_type, mode, expected_exception, expected_message
):
    if expected_exception:
        with pytest.raises(expected_exception, match=expected_message):
            validate_input(item, item_list, item_type, mode)
    else:
        validate_input(item, item_list, item_type, mode)


@pytest.mark.parametrize(
    "item, key, my_dict_list, expected_result",
    [
        (2, "key", [{"key": 1, "value": "A"}, {"key": 2, "value": "B"}], True),
        (3, "key", [{"key": 1, "value": "A"}, {"key": 2, "value": "B"}], False),
        ("A", "value", [{"key": 1, "value": "A"}, {"key": 2, "value": "B"}], True),
        ("C", "value", [{"key": 1, "value": "A"}, {"key": 2, "value": "B"}], False),
        (None, "key", [{"key": 1, "value": "A"}, {"key": None, "value": "B"}], True),
        (None, "value", [{"key": 1, "value": "A"}, {"key": 2, "value": None}], True),
    ],
)
def test_is_used(item, key, my_dict_list, expected_result):
    result = is_used(item, key, my_dict_list)
    assert result == expected_result


def test_save_metadata(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)
    # create data
    new_manager.initialize_data()

    # update metadata locally
    new_manager.accounts.append("test")
    new_manager.categories.append("test")
    new_manager.sub_categories.append("test")

    # save metadata
    new_manager.save_metadata()

    # load metadata
    new_manager.load_metadata()

    # check if new category is added
    for item in new_manager.metadata:
        assert "test" in new_manager.metadata[item]

    # remove metadata
    new_manager.accounts.remove("test")
    new_manager.categories.remove("test")
    new_manager.sub_categories.remove("test")

    # don't save
    new_manager.initialize_data()  # init to restore list values

    # check if new category is added
    for item in new_manager.metadata:
        assert "test" in new_manager.metadata[item]

    # remove metadata
    new_manager.accounts.remove("test")
    new_manager.categories.remove("test")
    new_manager.sub_categories.remove("test")

    # save
    new_manager.save_metadata()

    # load metadata
    new_manager.load_metadata()

    # check if new category is added
    for item in new_manager.metadata:
        assert "test" not in new_manager.metadata[item]


def test_add_remove_category(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)
    # create data
    new_manager.initialize_data()

    item = "test"

    new_manager.add_category(category=item)

    assert item in new_manager.categories

    with pytest.raises(ValueError):
        new_manager.add_category(category=item)

    with pytest.raises(ValueError):
        new_manager.add_category(category=9)

    with pytest.raises(ValueError):
        new_manager.remove_category(category="test2")

    with pytest.raises(ValueError):
        new_manager.remove_category(category="banktransfer")

    new_manager.remove_category(category=item)

    assert item not in new_manager.categories


def test_add_remove_subcategory(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)
    # create data
    new_manager.initialize_data()

    item = "test"

    new_manager.add_subcategory(subcategory=item)

    assert item in new_manager.sub_categories

    with pytest.raises(ValueError):
        new_manager.add_subcategory(subcategory=item)

    with pytest.raises(ValueError):
        new_manager.add_subcategory(subcategory=9)

    with pytest.raises(ValueError):
        new_manager.remove_subcategory(subcategory="test2")

    with pytest.raises(ValueError):
        new_manager.remove_subcategory(subcategory="evotec")

    new_manager.remove_subcategory(subcategory=item)

    assert item not in new_manager.sub_categories


def test_add_remove_account(create_empty_folder):
    new_manager = DataManager(data_folder=create_empty_folder)
    # create data
    new_manager.initialize_data()

    item = "test"

    new_manager.add_account(account=item)

    assert item in new_manager.accounts

    with pytest.raises(ValueError):
        new_manager.add_account(account=item)

    with pytest.raises(ValueError):
        new_manager.add_account(account=9)

    with pytest.raises(ValueError):
        new_manager.remove_account(account="test2")

    with pytest.raises(ValueError):
        new_manager.remove_account(account="evotec")

    new_manager.remove_account(account=item)

    assert item not in new_manager.accounts
