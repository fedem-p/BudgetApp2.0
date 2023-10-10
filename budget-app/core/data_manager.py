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
import csv
import json
import os

import pandas as pd

# TODO handle with pandas
EXAMPLE_DATA = [
    {
        "date": "2018-01-03",
        "type": "income",
        "amount": 94.0,
        "account": "N26",
        "category": "salary",
        "subcategory": "evotec",
        "note": "may",
    },
    {
        "date": "2018-01-02",
        "type": "income",
        "amount": 39.48,
        "account": "Wallet",
        "category": "gift",
        "subcategory": "family",
        "note": "christmas",
    },
    {
        "date": "2018-05-11",
        "type": "expense",
        "amount": -7.0,
        "account": "Wallet",
        "category": "bar",
        "subcategory": "alcohol",
        "note": "beer",
    },
    {
        "date": "2018-05-18",
        "type": "expense",
        "amount": -9.5,
        "account": "N26",
        "category": "transport",
        "subcategory": "public transport",
        "note": "bus",
    },
    {
        "date": "2018-05-11",
        "type": "expense",
        "amount": -7.0,
        "account": "Wallet",
        "category": "bar",
        "subcategory": "alcohol",
        "note": "wine",
    },
    {
        "date": "2018-05-18",
        "type": "expense",
        "amount": -9.5,
        "account": "Wallet",
        "category": "grocery",
        "subcategory": "food",
        "note": "penny",
    },
    {
        "date": "2020-12-10",
        "type": "expense",
        "amount": -50.0,
        "account": "N26",
        "category": "banktransfer",
        "subcategory": "",
        "note": "to Wallet",
    },
    {
        "date": "2020-12-16",
        "type": "income",
        "amount": 50.0,
        "account": "C24",
        "category": "banktransfer",
        "subcategory": "",
        "note": "from room",
    },
]
EXAMPLE_METADATA = {
    "accounts": ["N26", "C24", "Wallet"],
    "categories": ["salary", "gift", "bar", "transport", "grocery", "banktransfer", ""],
    "subcategories": ["food", "evotec", "family", "alcohol", "public transport", ""],
}

DATA_CSV = "data.csv"
METADATA_JSON = "metadata.json"


class DataManager:
    def __init__(self, data_folder: str = "../data"):
        # TODO check if it's a folder path
        self.data_folder = data_folder
        #TODO collect all self variables and initialize to none
        self.balances = None

    def initialize_data(self):
        if self.is_empty_data_folder():
            self.create_data_file()

        self.load_metadata()
        self.load_transactions()
        # if no data is found the files are populated with some example data
        # TODO: for now all data is loaded -> if performance becomes a problem explore other solutions
        self.accounts = self.metadata["accounts"]
        self.categories = self.metadata["categories"]
        self.sub_categories = self.metadata["subcategories"]

    def is_empty_data_folder(self):
        for file_name in os.listdir(self.data_folder):
            # TODO manage case in which only one of the two files is present
            if file_name == DATA_CSV or file_name == METADATA_JSON:
                return False
        return True

    def create_data_file(self):
        csv_file_path = os.path.join(self.data_folder, DATA_CSV)
        json_file_path = os.path.join(self.data_folder, METADATA_JSON)

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(EXAMPLE_DATA)

        # Use the to_csv() method to export the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)
        with open(json_file_path, "w") as jsonfile:
            json.dump(EXAMPLE_METADATA, jsonfile, indent=4)

    def load_transactions(self):
        data_df = self.load_csv()
        df_cleaned = data_df.fillna("")

        self.transactions = df_cleaned.to_dict(orient="records")

    def load_csv(self):
        data_df = pd.read_csv(os.path.join(self.data_folder, DATA_CSV))
        return data_df

    def load_metadata(self):
        with open(os.path.join(self.data_folder, METADATA_JSON), "r") as file:
            json_data = json.load(file)
        self.metadata = json_data

    def get_account_balance(self,account):
        if self.balances is not None:
            if account in self.balances:
                return self.balances[account]
            
        
        # generate balance
        self.update_balance(account)
        return self.balances[account]

    def update_balance(self,account):
        new_balance = 0
        if self.balances is None:
            self.balances = {}

        for transaction in self.transactions:
            if transaction['account'] == account:
                new_balance += transaction['amount']

        self.balances[account] = round(new_balance, 2)
                

