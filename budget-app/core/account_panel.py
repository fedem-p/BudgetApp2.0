"""Module to define the account page to insert in the bottom navbar of the app."""
import logging
import time

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

logger = logging.getLogger(__name__)


class AccountPage:
    """
    Class to define the App page that holds all the accounts
    and any functionality to add and remove accounts.
    """

    def __init__(self, data_manager: DataManager):
        logger.info("AccountPage: %s:  __init__", time.time())
        self.data_manager = data_manager
        self.accounts_list = MDList()
        self.accounts = self.data_manager.accounts
        self.base = MDBoxLayout()
        self.save_dialog = None
        self.delete_dialog = None

    def build_page(self):
        """Builds a page using a bottom navbar item and
        calls a function to generate the content of the page.

        Returns:
            MDBottomNavigationItem: Bottom navbar item.
        """
        logger.info("AccountPage: %s:  build_page", time.time())
        self.base.add_widget(self.generate_account_list())
        self.base.add_widget(
            MDFloatingActionButton(
                icon="plus",
                pos_hint={"right": 1, "bottom": 1},
                on_release=self.get_dialog_text_input,
            )
        )
        return MDBottomNavigationItem(
            self.base,
            name="accounts",
            text="Accounts",
            icon="bank",
            badge_icon="numeric-3",
        )

    def single_account_widget(self, account, description):
        """Generate a single widget to hold account name and balance.

        Args:
            account (str): account name
            description (str): account name and balance

        Returns:
            OneLineAvatarIconListItem: widget with icon, description and delete button.
        """
        logger.info("AccountPage: %s:  single_account_widget", time.time())
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="bank"),
            IconRightWidget(
                icon="delete",
                on_release=lambda x, item=[
                    account,
                    description,
                ]: self.get_confirmation_dialog(item),
            ),
            text=description,
            id=account,
        )

    def generate_account_list(self):
        """Generate a list of widgets to hold each account name and balance.

        Returns:
            MDScrollView: list widget with all account names and balances.
        """
        logger.info("AccountPage: %s:  generate_account_list", time.time())
        for account in self.accounts:
            description = f"{account} |\
                 Balance: {self.data_manager.get_account_balance(account=account)}$"

            self.accounts_list.add_widget(
                self.single_account_widget(account=account, description=description)
            )

        return MDScrollView(self.accounts_list)

    def add_new_account(self, account_name):
        """Add new account element to the list of accounts.

        Args:
            account_name (str): new account name.
        """
        logger.info("AccountPage: %s:  add_new_account", time.time())
        account_name = account_name.text
        # add new account to data manager
        self.data_manager.add_account(account=account_name)
        # define string to hold account name and balance
        description = f"{account_name} |\
             Balance: {self.data_manager.get_account_balance(account=account_name)}$"
        # add account to list
        self.accounts_list.add_widget(
            self.single_account_widget(account=account_name, description=description)
        )
        # dismiss input dialog
        self.save_dialog.dismiss()

    def delete_account(self, account_label):
        """Delete account element from the list of accounts.

        Args:
            input_list (list): list of two elements: account name and description.
        """
        logger.info("AccountPage: %s:  delete_account", time.time())
        account = account_label.text
        # description = input_list[1]
        # Remove the corresponding widget from the layout
        widget_to_remove = next(
            widget for widget in self.accounts_list.children if widget.id == account
        )
        self.accounts_list.remove_widget(widget_to_remove)
        self.data_manager.remove_account(account=account)

        # dismiss input dialog
        self.delete_dialog.dismiss()

    def get_dialog_text_input(self, instance):  # pylint: disable=W0613
        """Opens Pop-up box with a text field to insert new account name."""
        logger.info("AccountPage: %s:  get_dialog_text_input", time.time())
        if not self.save_dialog:
            # create text input
            text_input = MDTextField(hint_text="Enter a new account")
            # create dialog button
            self.save_dialog = DialogBuilder().build_dialog(
                title="Add new Account:",
                content=text_input,
                on_release_function=self.add_new_account,
            )

        self.save_dialog.open()

    def get_confirmation_dialog(self, item):
        """Opens Pop-up box with a text field to delete an account."""
        logger.info("AccountPage: %s:  get_confirmation_dialog", time.time())
        if not self.delete_dialog:
            # create text input
            display_text = MDLabel(text=item[0])
            # create dialog button
            self.delete_dialog = DialogBuilder().build_dialog(
                title="Delete this account?",
                content=display_text,
                on_release_function=self.delete_account,
            )

        self.delete_dialog.open()
