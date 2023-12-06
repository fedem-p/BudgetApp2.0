"""Module with all the validators for the data manager."""
from datetime import datetime


def validate_transaction(item, accounts, categories, sub_categories):
    """validate a transaction fields.

    Args:
        item (dict): transaction

    Raises:
        ValueError: Error for each field based on its value.
    """
    sample_transaction_keys = {
        "date",
        "type",
        "amount",
        "account",
        "category",
        "subcategory",
        "note",
    }

    if sample_transaction_keys != item.keys():
        raise ValueError("Transaction Error: dict key missing or extra.")

    if item["type"] not in {
        "income",
        "expense",
        "transfer",
    }:  # pylint: disable=raise-missing-from
        raise ValueError(
            f"Transaction Error: Unknown transaction type: {item['type']}."
        )

    try:
        _ = int(item["amount"])
    except ValueError:
        raise ValueError(  # pylint: disable=raise-missing-from
            f"Transaction Error: Amount must be float or int: {item['amount']}"
        )

    if int(item["amount"]) < 0:
        raise ValueError(
            f"Transaction Error: Amount must be a positive number: {item['amount']}"
        )

    for key, value in {
        "account": accounts,
        "category": categories,
        "subcategory": sub_categories,
    }.items():  # pylint: disable=raise-missing-from
        if item[key] not in value:
            raise ValueError(f"Transaction Error: Unknown {key}:{item[key]}.")

    date_format = "%Y/%m/%d"
    try:
        datetime.strptime(item["date"], date_format)
    except ValueError:
        raise ValueError(  # pylint: disable=raise-missing-from
            f"Transaction Error: Invalid date format. Must be in {date_format}."
        )


def validate_input(item, item_list, item_type, mode="add"):
    """Utility function validate the input before updating data.

    - checks if item is correct type
    - if mode "add" checks if item isn't already present in the list.
    - if mode "remove" checks if item is present in the list.

    Args:
        item: item to check (e.g. str)
        item_list (list): list of present items.
        item_type (type): type of the item that is expected.
        mode (str, optional): mode of the check. Defaults to "add".

    Raises:
        ValueError: Mode Error: Mode can only be 'add' or 'remove'
        ValueError: Type Error: {item} is not type {item_type}
        ValueError: Integrity Error: Item: {item} already exists!
        ValueError: 404 Error: Item: {item} not found!
    """
    if mode not in {"add", "remove"}:
        raise ValueError("Mode Error: Mode can only be 'add' or 'remove'!")

    if not isinstance(item, item_type):
        raise ValueError(f"Type Error: {item} is not type {item_type}")

    if mode == "add":
        if item in item_list:
            raise ValueError(f"Integrity Error: Item: {item} already exists!")

    if mode == "remove":
        if item not in item_list:
            raise ValueError(f"404 Error: Item: {item} not found!")


def is_used(item, key, my_dict_list):
    """Utility function to check whether an item is currently used or not.

    Args:
        item: item to check.
        key (str): dictionary key to use (e.g "category", "account",..).
        my_dict_list (list): list of dictionaries (e.g. transactions, accounts)

    Returns:
        bool: if found it means it's in use.
    """
    found = any(d.get(key) == item for d in my_dict_list)
    return found
