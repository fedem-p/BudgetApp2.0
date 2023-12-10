"""Module to define the transaction page to insert in the bottom navbar of the app."""
import logging
import time
from datetime import datetime

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    IconLeftWidget,
    IconRightWidget,
    MDList,
    OneLineAvatarIconListItem,
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from .data_manager import DataManager
from .utils.dialogbox import DialogBuilder
from .utils.dropdown_list import DropdownBuilder
from .utils.utils import dict2str, str2dict
from .utils.validator import validate_transaction

logger = logging.getLogger(__name__)


class TransactionPage:
    """
    Class to define the App page that holds all the transactions
    and any functionality to add and remove transactions.
    """

    def __init__(self, data_manager: DataManager):
        logger.info("TransactionPage: %s:  __init__", time.time())
        self.data_manager = data_manager
        self.transaction_list = MDList()
        self.transactions = self.data_manager.transactions
        self.base = MDBoxLayout()
        self.save_dialog = None
        self.delete_dialog = None
        self.transfer_dialog = None

    def build_page(self):
        """Builds a page using a bottom navbar item and
        calls a function to generate the transactions list.

        Returns:
            MDBottomNavigationItem: Bottom navbar item.
        """
        logger.info("TransactionPage: %s:  build_page", time.time())
        self.base.add_widget(self.generate_transactions_list())
        # pylint: disable=R0801
        self.base.add_widget(  # pylint: disable=R0801
            MDFloatingActionButton(
                icon="swap-horizontal",
                pos_hint={"right": 1, "bottom": 1},
                on_release=self.get_dialog_transfer_input,
            )
        )
        self.base.add_widget(  # pylint: disable=R0801
            MDFloatingActionButton(
                icon="plus",
                pos_hint={"right": 1, "bottom": 1},
                on_release=self.get_dialog_transaction_input,
            )
        )
        # pylint: enable=R0801
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
        logger.info("TransactionPage: %s:  generate_transactions_list", time.time())
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
        logger.info("TransactionPage: %s:  single_transaction_widget", time.time())
        description = dict2str(transaction)

        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="swap-horizontal"),
            IconRightWidget(
                icon="delete",
                on_release=lambda x, item=transaction: self.get_confirmation_dialog(
                    item
                ),
            ),
            text=description,
        )

    def delete_transaction(self, transaction_label):
        """Delete transaction element from the list of transactions.

        Args:
            input_list (list): list of two elements: transaction dict and description.
        """
        logger.info("TransactionPage: %s:  delete_transaction", time.time())
        transaction_text = transaction_label.text
        transaction = str2dict(transaction_label.text)
        # Remove the corresponding widget from the layout
        widget_to_remove = next(
            widget
            for widget in self.transaction_list.children
            if widget.text == transaction_text
        )
        self.transaction_list.remove_widget(widget_to_remove)
        self.data_manager.remove_transaction(transaction=transaction)

        self.delete_dialog.dismiss()

    def add_new_transaction(self, box):
        """Add new transaction element to the list of transactions.

        Args:
            transaction (dict): new transaction dict.
        """
        logger.info("TransactionPage: %s:  add_new_transaction", time.time())
        transaction = {
            "date": box.ids["date"].text,
            "type": box.ids["type"].text,
            "amount": box.ids["amount"].text,
            "account": box.ids["account"].text,
            "category": box.ids["category"].text,
            "subcategory": box.ids["subcategory"].text,
            "note": box.ids["note"].text,
        }

        # add new transaction to data manager
        self.data_manager.add_transaction(transaction=transaction)
        # add transaction to list
        self.transaction_list.add_widget(
            self.single_transaction_widget(transaction=transaction)
        )
        # dismiss input dialog
        self.save_dialog.dismiss()

    def get_dialog_transaction_input(self, instance):  # pylint: disable=W0613
        """Opens Pop-up box with a text field to insert new transaction name."""
        logger.info("TransactionPage: %s:  get_dialog_transaction_input", time.time())
        if not self.save_dialog:
            # create text input for each field
            date_input = MDTextField(
                id="date",
                hint_text="Enter a date",
                validator="date",
                date_format="yyyy/mm/dd",
                text=datetime.now().strftime("%Y/%m/%d"),
                required=True,
            )
            type_input = DropdownBuilder(
                main_id="type", items=["income", "expense"]
            ).get_dropdown_list()
            amount_input = MDTextField(
                id="amount", hint_text="Enter a numeric amount", required=True
            )
            account_input = DropdownBuilder(
                main_id="account",
                initial_text="Enter an account",
                items=self.data_manager.accounts,
            ).get_dropdown_list()
            category_input = DropdownBuilder(
                main_id="category",
                initial_text="Enter a category",
                items=self.data_manager.categories,
            ).get_dropdown_list()
            subcategory_input = DropdownBuilder(
                main_id="subcategory",
                initial_text="Enter a subcategory",
                items=self.data_manager.sub_categories,
            ).get_dropdown_list()
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
            self.save_dialog = DialogBuilder().build_save_dialog(
                title="Add new Transaction:",
                content=my_box,
                on_release_function=self.add_new_transaction,
            )

        self.save_dialog.open()

    def get_confirmation_dialog(self, item):
        """Opens Pop-up box with a text field to delete a transaction."""
        logger.info("TransactionPage: %s:  get_confirmation_dialog", time.time())
        # create text input
        display_text = MDLabel(text=dict2str(item))
        # create dialog button
        self.delete_dialog = DialogBuilder().build_save_dialog(
            title="Delete this transaction?",
            content=display_text,
            on_release_function=self.delete_transaction,
        )

        self.delete_dialog.open()

    def get_dialog_transfer_input(self, instance):  # pylint: disable=W0613
        """Opens Pop-up box with a text field to insert new transfer."""
        logger.info("TransactionPage: %s:  get_dialog_transfer_input", time.time())
        if not self.transfer_dialog:
            # create text input for each field
            date_input = MDTextField(
                id="date",
                hint_text="Enter a date",
                validator="date",
                date_format="yyyy/mm/dd",
                text=datetime.now().strftime("%Y/%m/%d"),
                required=True,
            )
            amount_input = MDTextField(
                id="amount", hint_text="Enter a numeric amount", required=True
            )
            from_account = DropdownBuilder(
                main_id="from-account",
                items=self.data_manager.accounts,
                initial_text="(FROM) Enter withdraw account",
            ).get_dropdown_list()
            to_account = DropdownBuilder(
                main_id="to-account",
                initial_text="(TO) Enter deposit account",
                items=self.data_manager.accounts,
            ).get_dropdown_list()
            note_input = MDTextField(id="note", hint_text="Enter any extra information")

            my_box = MDBoxLayout(
                date_input,
                amount_input,
                from_account,
                to_account,
                note_input,
                orientation="vertical",
                # spacing="12dp",
                size_hint_y=None,
                height="420dp",
            )

            # create dialog button
            self.transfer_dialog = DialogBuilder().build_save_dialog(
                title="Add new Transfer:",
                content=my_box,
                on_release_function=self.transfer_funds,
            )

        self.transfer_dialog.open()

    def transfer_funds(self, box):
        """Add new transfer between two accounts to the list of transactions.

        Args:
            box (dict): widget with the inputs of the dialog box.
        """
        logger.info("TransactionPage: %s:  transfer_funds", time.time())

        date = box.ids["date"].text
        amount = box.ids["amount"].text
        from_account = box.ids["from-account"].text
        to_account = box.ids["to-account"].text
        note = box.ids["note"].text

        if from_account == to_account:
            raise ValueError("Accounts must be different!")

        if "(FROM)" in from_account or "(TO)" in to_account:
            raise ValueError("You must select an account!")

        transaction_from = {
            "date": date,
            "type": "withdraw",
            "amount": amount,
            "account": from_account,
            "category": "banktransfer",
            "subcategory": "banktransfer",
            "note": note,
        }
        transaction_to = {
            "date": date,
            "type": "deposit",
            "amount": amount,
            "account": to_account,
            "category": "banktransfer",
            "subcategory": "banktransfer",
            "note": note,
        }

        # check that both accounts exist
        validate_transaction(
            item=transaction_from,
            accounts=self.data_manager.accounts,
            categories=self.data_manager.categories,
            sub_categories=self.data_manager.sub_categories,
        )
        validate_transaction(
            item=transaction_to,
            accounts=self.data_manager.accounts,
            categories=self.data_manager.categories,
            sub_categories=self.data_manager.sub_categories,
        )

        # add new transactions to data manager
        self.data_manager.add_transaction(transaction=transaction_from)
        self.data_manager.add_transaction(transaction=transaction_to)
        # add transactions to list
        self.transaction_list.add_widget(
            self.single_transaction_widget(transaction=transaction_from)
        )
        self.transaction_list.add_widget(
            self.single_transaction_widget(transaction=transaction_to)
        )
        # dismiss input dialog
        self.transfer_dialog.dismiss()
