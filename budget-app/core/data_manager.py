"""
Data manager module

data files:
    - main data -> csv file with all transactions
    - additional info -> json file with accounts names, categories and subcategories.

operations:
    - create data files if not present
    - add info to data files
    - create data files from input csv
    - export data files
    - load only the necessary data statistics

"""

import json
import os
from datetime import datetime

import pandas as pd

from .utils.dummy_data import EXAMPLE_DATA, EXAMPLE_METADATA

DATA_CSV = "data.csv"
METADATA_JSON = "metadata.json"


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


class DataManager:
    """Data manager to handle the data loading, saving and updating."""

    def __init__(self, data_folder: str = "../data"):
        # TODO check if it's a folder path # pylint: disable=W0511
        self.data_folder = data_folder
        self.balances = None
        self.accounts = None
        self.categories = None
        self.sub_categories = None
        self.transactions = None
        self.metadata = None

    def initialize_data(self):
        """Initialize all data, by either loading it or generating a dummy example."""
        if self.is_empty_data_folder():
            self.create_data_file()

        self.load_metadata()
        self.load_transactions()
        # if no data is found the files are populated with some example data
        # TODO: for now all data is loaded  # pylint: disable=W0511
        # if performance becomes a problem explore other solutions
        self.accounts = self.metadata["accounts"]
        self.categories = self.metadata["categories"]
        self.sub_categories = self.metadata["subcategories"]

    def is_empty_data_folder(self):
        """Utility function that checks if the data folder is empty.

        Returns:
            bool: checks if the data folder is empty.
        """
        for file_name in os.listdir(self.data_folder):
            # TODO manage case in which only one of the two files is present # pylint: disable=W0511
            if file_name in {DATA_CSV, METADATA_JSON}:
                return False
        return True

    def create_data_file(self):
        """Utility function that creates dummy data files."""
        csv_file_path = os.path.join(self.data_folder, DATA_CSV)
        json_file_path = os.path.join(self.data_folder, METADATA_JSON)

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(EXAMPLE_DATA)

        # Use the to_csv() method to export the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)
        with open(json_file_path, "w", encoding="utf8") as jsonfile:
            json.dump(EXAMPLE_METADATA, jsonfile, indent=4)

    def load_transactions(self):
        """Load transactins from csv file."""
        data_df = self.load_csv()
        df_cleaned = data_df.fillna("")

        self.transactions = df_cleaned.to_dict(orient="records")

    def load_csv(self):
        """Load csv data file.

        Returns:
            pandas.DataFrame: return a pandas dataframe of the csv file.
        """
        data_df = pd.read_csv(os.path.join(self.data_folder, DATA_CSV))
        return data_df

    def load_metadata(self):
        """Load metadata json file."""
        with open(
            os.path.join(self.data_folder, METADATA_JSON), "r", encoding="utf8"
        ) as file:
            json_data = json.load(file)
        self.metadata = json_data

    def get_account_balance(self, account):
        """Get the balance value of a certain account.

        Args:
            account (str): account name.

        Returns:
            float: balance value for the requested account.
        """
        if self.balances is not None:
            if account in self.balances:
                return self.balances[account]

        # generate balance
        self.update_balance(account)
        return self.balances[account]

    def update_balance(self, account):
        """update balances for each account.

        Args:
            account (str): account name.
        """
        new_balance = 0
        if self.balances is None:
            self.balances = {}

        for transaction in self.transactions:
            if transaction["account"] == account:
                new_balance += transaction["amount"]

        self.balances[account] = round(new_balance, 2)

    def save_metadata(self):
        """save metadata in a json file."""
        # TODO keep last n version of a file # pylint: disable=W0511
        # update metadata
        self.metadata["accounts"] = self.accounts
        self.metadata["categories"] = self.categories
        self.metadata["subcategories"] = self.sub_categories

        with open(
            os.path.join(self.data_folder, METADATA_JSON), "w", encoding="utf8"
        ) as file:
            json.dump(self.metadata, file, indent=4)

    def save_transactions(self):
        """save transactions in a csv file."""
        # TODO keep last n version of a file # pylint: disable=W0511
        csv_file_path = os.path.join(self.data_folder, DATA_CSV)
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(self.transactions)

        # Use the to_csv() method to export the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)

    def add_category(self, category):
        """Add a new category to the metadata.

        Args:
            category (str): category name.
        """
        validate_input(
            item=category, item_list=self.categories, item_type=str, mode="add"
        )

        # add category
        self.categories.append(category)

        # save new metadata
        self.save_metadata()

    def add_subcategory(self, subcategory):
        """Add a new subcategory to the metadata.

        Args:
            subcategory (str): subcategory name.
        """
        validate_input(
            item=subcategory, item_list=self.sub_categories, item_type=str, mode="add"
        )

        # add category
        self.sub_categories.append(subcategory)

        # save new metadata
        self.save_metadata()

    def add_account(self, account):
        """Add a new account to the metadata.

        Args:
            account (str): account name.
        """
        validate_input(item=account, item_list=self.accounts, item_type=str, mode="add")

        # add category
        self.accounts.append(account)

        # save new metadata
        self.save_metadata()

    def add_transaction(self, transaction):
        """Add a new transaction to the data.

        Args:
            transaction (dict): transaction dict.
        """
        validate_input(
            item=transaction, item_list=self.transactions, item_type=dict, mode="add"
        )

        self.validate_transaction(item=transaction)

        transaction["amount"] = int(transaction["amount"])

        # add category
        self.transactions.append(transaction)

        # save new metadata
        self.save_transactions()

    def remove_category(self, category):
        """Remove a category from the metadata.

        Args:
            category (str): category name.

        Raises:
            ValueError: If category is still used.
        """
        validate_input(
            item=category, item_list=self.categories, item_type=str, mode="remove"
        )

        # check if item is used
        if is_used(item=category, key="category", my_dict_list=self.transactions):
            raise ValueError(f"Integrity Error: Item: {category} is still in use!")

        # remove category
        self.categories.remove(category)

        # save new metadata
        self.save_metadata()

    def remove_subcategory(self, subcategory):
        """Remove a subcategory from the metadata.

        Args:
            subcategory (str): subcategory name.

        Raises:
            ValueError: If subcategory is still used.
        """
        validate_input(
            item=subcategory,
            item_list=self.sub_categories,
            item_type=str,
            mode="remove",
        )

        # check if item is used
        if is_used(item=subcategory, key="subcategory", my_dict_list=self.transactions):
            raise ValueError(f"Integrity Error: Item: {subcategory} is still in use!")

        # remove subcategory
        self.sub_categories.remove(subcategory)

        # save new metadata
        self.save_metadata()

    def remove_account(self, account):
        """Remove a account from the metadata.

        Args:
            account (str): account name.

        Raises:
            ValueError: If account is still used.
        """
        validate_input(
            item=account, item_list=self.accounts, item_type=str, mode="remove"
        )

        # check if item is used
        if is_used(item=account, key="account", my_dict_list=self.transactions):
            raise ValueError(f"Integrity Error: Item: {account} is still in use!")

        # remove account
        self.accounts.remove(account)

        # save new metadata
        self.save_metadata()

    def remove_transaction(self, transaction):
        """Remove a transaction to the data.

        Args:
            transaction (dict): transaction dict.
        """
        validate_input(
            item=transaction, item_list=self.transactions, item_type=dict, mode="remove"
        )

        # remove transaction
        self.transactions.remove(transaction)

        # save new metadata
        self.save_transactions()

    def validate_transaction(self, item):
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

        if item["type"] not in {"income", "expense", "transfer"}: # pylint: disable=raise-missing-from
            raise ValueError( 
                f"Transaction Error: Unknown transaction type: {item['type']}."
            )

        try:
            _ = int(item["amount"])
        except ValueError:
            raise ValueError(
                f"Transaction Error: Amount must be float or int: {item['amount']}"
            )

        if int(item["amount"]) < 0:
            raise ValueError(
                f"Transaction Error: Amount must be a positive number: {item['amount']}"
            )

        for key, value in {
            "account": self.accounts,
            "category": self.categories,
            "subcategory": self.sub_categories,
        }.items(): # pylint: disable=raise-missing-from
            if item[key] not in value:
                raise ValueError(f"Transaction Error: Unknown {key}:{item[key]}.")

        date_format = "%Y/%m/%d"
        try:
            datetime.strptime(item["date"], date_format)
        except ValueError:
            raise ValueError(
                f"Transaction Error: Invalid date format. Must be in {date_format}."
            )
