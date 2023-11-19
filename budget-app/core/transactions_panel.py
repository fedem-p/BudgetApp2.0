from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.list import (
    IconLeftWidget,
    IconRightWidget,
    MDList,
    OneLineAvatarIconListItem,
    OneLineListItem,
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from .data_manager import DataManager


class TransactionPage:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.transaction_list = MDList()
        self.transactions = self.data_manager.transactions

    def build_page(self):
        return MDBottomNavigationItem(
            self.generate_transactions_list(),
            name="transactions",
            text="Transactions",
            icon="format-list-bulleted",
        )

    def generate_transactions_list(self):
        for transaction in self.transactions:
            txt = f"Date:        {transaction['date']},\
                    Type:        {transaction['type']},\
                    Amount:      {transaction['amount']}$,\
                    Account:     {transaction['account']},\
                    Category:    {transaction['category']},\
                    SubCategory: {transaction['subcategory']},\
                    Notes:       {transaction['note']}"

            self.transaction_list.add_widget(
                OneLineListItem(
                    # IconRightWidget(
                    #     icon="delete"
                    # ),
                    text=txt,
                )
            )
        return MDScrollView(self.transaction_list)
