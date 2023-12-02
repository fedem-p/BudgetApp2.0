"""Module to define the account page to insert in the bottom navbar of the app."""
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
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


class AccountPage:
    """
    Class to define the App page that holds all the accounts
    and any functionality to add and remove accounts.
    """

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.accounts_list = MDList()
        self.accounts = self.data_manager.accounts
        self.base = BoxLayout()
        self.dialog = None

    def build_page(self):
        """Builds a page using a bottom navbar item and
        calls a function to generate the content of the page.

        Returns:
            MDBottomNavigationItem: Bottom navbar item.
        """
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
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="bank"),
            IconRightWidget(
                icon="delete",
                on_release=lambda x, item=[account, description]: self.delete_account(
                    item
                ),
            ),
            text=description,
        )

    def generate_account_list(self):
        """Generate a list of widgets to hold each account name and balance.

        Returns:
            MDScrollView: list widget with all account names and balances.
        """
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
        self.dialog.dismiss()

    def delete_account(self, input_list):
        """Delete account element from the list of accounts.

        Args:
            input_list (list): list of two elements: account name and description.
        """
        account = input_list[0]
        description = input_list[1]
        # Remove the corresponding widget from the layout
        widget_to_remove = next(
            widget
            for widget in self.accounts_list.children
            if widget.text == description
        )
        self.accounts_list.remove_widget(widget_to_remove)
        self.data_manager.remove_account(account=account)

    def get_dialog_text_input(self, instance):  # pylint: disable=W0613
        """Opens Pop-up box with a text field to insert new account name."""

        if not self.dialog:
            # create text input
            text_input = MDTextField(hint_text="Enter a new account")
            # create dialog button
            self.dialog = MDDialog(
                title="Add new Account:",
                type="custom",
                content_cls=text_input,
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="Save",
                        on_release=lambda x, item=text_input: self.add_new_account(
                            account_name=item.text
                        ),
                    ),
                ],
            )

        self.dialog.open()
