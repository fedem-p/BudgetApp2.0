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
import logging
import os
import time

import pandas as pd

from .utils.dummy_data import EXAMPLE_DATA, EXAMPLE_METADATA
from .utils.validator import is_used, validate_input, validate_transaction

DATA_CSV = "data.csv"
METADATA_JSON = "metadata.json"

logger = logging.getLogger(__name__)


class DataManager:
    """Data manager to handle the data loading, saving and updating."""

    def __init__(self, data_folder: str = "../data"):
        logger.info("DataManager: %s:  Init", time.time())
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
        logger.info("DataManager: %s:  Init data", time.time())
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
        logger.info("DataManager: %s:  is_empty_data_folder", time.time())

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
        logger.info("DataManager: %s:  create_data_file", time.time())
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
        logger.info("DataManager: %s:  load_transactions", time.time())
        data_df = self.load_csv()
        df_cleaned = data_df.fillna("")

        self.transactions = df_cleaned.to_dict(orient="records")

    def load_csv(self):
        """Load csv data file.

        Returns:
            pandas.DataFrame: return a pandas dataframe of the csv file.
        """
        logger.info("DataManager: %s:  load_csv", time.time())
        data_df = pd.read_csv(os.path.join(self.data_folder, DATA_CSV))
        return data_df

    def load_metadata(self):
        """Load metadata json file."""
        logger.info("DataManager: %s:  load_metadata", time.time())
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
        logger.info("DataManager: %s:  get_account_balance", time.time())
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
        logger.info("DataManager: %s:  update_balance", time.time())
        new_balance = 0
        if self.balances is None:
            self.balances = {}

        for transaction in self.transactions:
            if transaction["account"] == account:
                new_balance += transaction["amount"]

        self.balances[account] = round(new_balance, 2)

    def save_metadata(self):
        """save metadata in a json file."""
        logger.info("DataManager: %s:  save_metadata", time.time())
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
        logger.info("DataManager: %s:  save_transactions", time.time())
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
        logger.info("DataManager: %s:  add_category", time.time())
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
        logger.info("DataManager: %s:  add_subcategory", time.time())
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
        logger.info("DataManager: %s:  add_account", time.time())
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
        logger.info("DataManager: %s:  add_transaction", time.time())
        validate_input(
            item=transaction, item_list=self.transactions, item_type=dict, mode="add"
        )

        validate_transaction(
            item=transaction,
            accounts=self.accounts,
            categories=self.categories,
            sub_categories=self.sub_categories,
        )

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
        logger.info("DataManager: %s:  remove_category", time.time())
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
        logger.info("DataManager: %s:  remove_subcategory", time.time())
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
        logger.info("DataManager: %s:  remove_account", time.time())
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
        logger.info("DataManager: %s:  remove_transaction", time.time())
        validate_input(
            item=transaction, item_list=self.transactions, item_type=dict, mode="remove"
        )

        # remove transaction
        self.transactions.remove(transaction)

        # save new metadata
        self.save_transactions()
