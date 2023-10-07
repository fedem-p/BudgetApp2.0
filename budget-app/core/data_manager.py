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
    ["date", "type", "amount", "account", "category", "subcategory", "note"],
    ["2018-01-03", "income", 94, "N26", "salary", "evotec", "may"],
    ["2018-01-02", "income", 39.48, "wallet", "gift", "family", "christmas"],
    ["2018-05-11", "expense", -7, "wallet", "bar", "alcohol", "beer"],
    ["2018-05-18", "expense", -9.5, "N26", "transport", "public transport", "bus"],
    ["2018-05-11", "expense", -7, "wallet", "bar", "alcohol", "wine"],
    ["2018-05-18", "expense", -9.5, "wallet", "grocery", "food", "penny"],
    ["2020-12-10", "expense", -50, "N26", "banktransfer", "", "to wallet"],
    ["2020-12-16", "income", 50, "C24", "banktransfer", "", "from room"],
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

    def initialize_data(self):
        if self.is_empty_data_folder():
            self.create_data_file()

        self.load_metadata()
        # if no data is found the files are populated with some example data
        # TODO: for now all data is loaded -> if performance becomes a problem explore other solutions
        # self.transactions = self.load_transactions()
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

        with open(csv_file_path, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(EXAMPLE_DATA)
        with open(json_file_path, "w") as jsonfile:
            json.dump(EXAMPLE_METADATA, jsonfile, indent=4)

    def load_transactions(self):
        pass

    def load_csv(self):
        csv_data = pd.read_csv(os.path.join(self.data_folder, DATA_CSV))
        return csv_data

    def load_metadata(self):
        with open(os.path.join(self.data_folder, METADATA_JSON), "r") as file:
            json_data = json.load(file)
        self.metadata = json_data
