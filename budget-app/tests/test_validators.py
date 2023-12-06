"""Tests for the data manager module."""
import os
import sys

import pytest

# Get the directory containing your module
module_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# sys.path.append('../')
sys.path.insert(0, module_directory)
# pylint: disable=C0116, W0621
from core.data_manager import DataManager  # pylint: disable=C0413,E0401
from core.utils.validator import (  # pylint: disable=C0413,E0401
    is_used,
    validate_input,
    validate_transaction,
)


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
        (
            {"test": 4},
            [{"test3": 1}, {"test2": 2}, {"test1": 3}],
            dict,
            "add",
            None,
            None,
        ),
        (
            {"test2": 2},
            [{"test3": 1}, {"test2": 2}, {"test1": 3}],
            dict,
            "remove",
            None,
            None,
        ),
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
def test_validate_input(  # pylint: disable=R0913
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


@pytest.mark.parametrize(
    "item, expected_exception",
    [
        (
            {
                "date": "2018/01/03",
                "type": "income",
                "amount": 94.0,
                "account": "N26",
                "category": "salary",
                "subcategory": "evotec",
                "note": "may",
            },
            None,
        ),
        (
            {
                "date": "2018/01/03",
                "type": "income",
                "account": "N26",
                "category": "salary",
                "subcategory": "evotec",
                "note": "may",
            },
            ValueError,
        ),
        (
            {
                "date": "2018/01/03",
                "type": "invalid_type",
                "amount": 94.0,
                "account": "N26",
                "category": "salary",
                "subcategory": "evotec",
                "note": "may",
            },
            ValueError,
        ),
        (
            {
                "date": "2018/01/03",
                "type": "income",
                "amount": "invalid_amount",
                "account": "N26",
                "category": "salary",
                "subcategory": "evotec",
                "note": "may",
            },
            ValueError,
        ),
        (
            {
                "date": "2018/01/03",
                "type": "income",
                "amount": -94.0,
                "account": "N26",
                "category": "salary",
                "subcategory": "evotec",
                "note": "may",
            },
            ValueError,
        ),
        (
            {
                "date": "2018/01/03",
                "type": "income",
                "amount": 94.0,
                "account": "Unknown_Account",
                "category": "salary",
                "subcategory": "evotec",
                "note": "may",
            },
            ValueError,
        ),
        (
            {
                "date": "01-03-2018",
                "type": "income",
                "amount": 94.0,
                "account": "N26",
                "category": "salary",
                "subcategory": "evotec",
                "note": "may",
            },
            ValueError,
        ),
    ],
)
def test_validate_transaction(create_empty_folder, item, expected_exception):
    new_manager = DataManager(data_folder=create_empty_folder)
    # create data
    new_manager.initialize_data()
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            validate_transaction(
                item=item,
                accounts=new_manager.accounts,
                categories=new_manager.categories,
                sub_categories=new_manager.sub_categories,
            )
    else:
        assert (
            validate_transaction(
                item=item,
                accounts=new_manager.accounts,
                categories=new_manager.categories,
                sub_categories=new_manager.sub_categories,
            )
            is None
        )
