"""Module to define the transaction page to insert in the bottom navbar of the app."""
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView

from .data_manager import DataManager


class TransactionPage:
    """
    Class to define the App page that holds all the transactions
    and any functionality to add and remove transactions.
    """

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.transaction_list = MDList()
        self.transactions = self.data_manager.transactions
        self.base = BoxLayout()

    def build_page(self):
        """Builds a page using a bottom navbar item and
        calls a function to generate the transactions list.

        Returns:
            MDBottomNavigationItem: Bottom navbar item.
        """
        self.base.add_widget(self.generate_transactions_list())
        self.base.add_widget(
            MDFloatingActionButton(icon="plus", pos_hint={"right": 1, "bottom": 1})
        )
        return MDBottomNavigationItem(
            self.base,
            name="transactions",
            text="Transactions",
            icon="format-list-bulleted",
        )

    def generate_transactions_list(self):
        """Gets the list of transactions from the data manager
        and returns a list of widgets holding each transaction information.

        Returns:
            MDScrollView: List of widget with transactions information.
        """
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
