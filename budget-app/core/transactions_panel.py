"""Module to define the transaction page to insert in the bottom navbar of the app."""
from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import (
    IconLeftWidget,
    IconRightWidget,
    MDList,
    OneLineAvatarIconListItem,
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

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
        self.dialog = None

    def build_page(self):
        """Builds a page using a bottom navbar item and
        calls a function to generate the transactions list.

        Returns:
            MDBottomNavigationItem: Bottom navbar item.
        """
        self.base.add_widget(self.generate_transactions_list())
        self.base.add_widget(
            MDFloatingActionButton(
                icon="plus",
                pos_hint={"right": 1, "bottom": 1},
                on_release=self.get_dialog_text_input,
            )
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
            self.transaction_list.add_widget(
                self.single_transaction_widget(transaction=transaction)
            )
        return MDScrollView(self.transaction_list)

    def single_transaction_widget(self, transaction):
        """Generate a single widget to hold the transaction details.

        Args:
            transaction (dict): transaction dictionary.

        Returns:
            OneLineAvatarIconListItem: widget with icon, details and delete button.
        """
        description = f"Date:        {transaction['date']},\
                    Type:        {transaction['type']},\
                    Amount:      {transaction['amount']}$,\
                    Account:     {transaction['account']},\
                    Category:    {transaction['category']},\
                    SubCategory: {transaction['subcategory']},\
                    Notes:       {transaction['note']}"

        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="swap-horizontal"),
            IconRightWidget(
                icon="delete",
                on_release=lambda x, item=[
                    transaction,
                    description,
                ]: self.delete_transaction(item),
            ),
            text=description,
        )

    def delete_transaction(self, input_list):
        """Delete transaction element from the list of transactions.

        Args:
            input_list (list): list of two elements: transaction dict and description.
        """
        transaction = input_list[0]
        description = input_list[1]
        # Remove the corresponding widget from the layout
        widget_to_remove = next(
            widget
            for widget in self.transaction_list.children
            if widget.text == description
        )
        self.transaction_list.remove_widget(widget_to_remove)
        self.data_manager.remove_transaction(transaction=transaction)

    def add_new_transaction(self, box):
        """Add new transaction element to the list of transactions.

        Args:
            transaction (dict): new transaction dict.
        """
        transaction = {
            "date": box.ids["date"].text,
            "type": box.ids["type"].text,
            "amount": box.ids["amount"].text,
            "account": box.ids["account"].text,
            "category": box.ids["category"].text,
            "subcategory": box.ids["subcategory"].text,
            "note": box.ids["note"].text,
        }

        # add new account to data manager
        self.data_manager.add_transaction(transaction=transaction)
        # add account to list
        self.transaction_list.add_widget(
            self.single_transaction_widget(transaction=transaction)
        )
        # dismiss input dialog
        self.dialog.dismiss()

    def get_dialog_text_input(self, instance):  # pylint: disable=W0613
        """Opens Pop-up box with a text field to insert new transaction name."""

        if not self.dialog:
            # create text input
            date_input = MDTextField(
                id="date",
                hint_text="Enter a date",
                validator="date",
                date_format="yyyy/mm/dd",
                text=datetime.now().strftime("%Y/%m/%d"),
                required=True,
            )
            type_input = MDTextField(
                id="type", hint_text="income / expense / transfer", required=True
            )
            amount_input = MDTextField(
                id="amount", hint_text="Enter a numeric amount", required=True
            )
            account_input = MDTextField(
                id="account", hint_text="Enter an account", required=True
            )
            category_input = MDTextField(
                id="category", hint_text="Enter a category", required=True
            )
            subcategory_input = MDTextField(
                id="subcategory", hint_text="Enter a subcategory", required=True
            )
            note_input = MDTextField(id="note", hint_text="Enter any extra information")

            my_box = MDBoxLayout(
                date_input,
                type_input,
                amount_input,
                account_input,
                category_input,
                subcategory_input,
                note_input,
                orientation="vertical",
                # spacing="12dp",
                size_hint_y=None,
                height="420dp",
            )

            # create dialog button
            self.dialog = MDDialog(
                title="Add new Transaction:",
                type="custom",
                content_cls=my_box,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Save",
                        on_release=lambda x, item=my_box: self.add_new_transaction(
                            box=item
                        ),
                    ),
                ],
            )

        self.dialog.open()
