from kivymd.uix.bottomnavigation import MDBottomNavigationItem
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
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.accounts_list = MDList()
        self.accounts = self.data_manager.accounts

    def build_page(self):
        return MDBottomNavigationItem(
            self.generate_account_list(),
            name="accounts",
            text="Accounts",
            icon="bank",
            badge_icon="numeric-3",
        )

    def single_account_widget(self, account, txt):
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="bank"),
            IconRightWidget(
                icon="delete",
                on_release=lambda x, item=[account, txt]: self.delete_account(item),
            ),
            text=txt,
        )

    def generate_account_list(self):
        for account in self.accounts:
            txt = f"{account} | Balance: {self.data_manager.get_account_balance(account=account)}$"

            self.accounts_list.add_widget(
                self.single_account_widget(account=account, txt=txt)
            )
        self.accounts_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"),
                text="Add a new account",
                on_release=self.update_account_list,
            )
        )

        return MDScrollView(self.accounts_list)

    def update_account_list(self, instance):
        text_input = MDTextField(hint_text="Enter a new account")
        text_input.on_text_validate = lambda: self.add_new_account(
            text_input, text_input.text
        )
        self.accounts_list.remove_widget(instance)
        self.accounts_list.add_widget(text_input)

    def add_new_account(self, text_input, text):
        self.accounts_list.remove_widget(text_input)
        self.data_manager.add_account(account=text)
        txt = (
            f"{text} | Balance: {self.data_manager.get_account_balance(account=text)}$"
        )
        self.accounts_list.add_widget(self.single_account_widget(account=text, txt=txt))
        self.accounts_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"),
                text="Add a new account",
                on_release=self.update_account_list,
            )
        )

    def delete_account(self, input_list):
        account = input_list[0]
        txt = input_list[1]
        print(account)
        print(txt)
        # Remove the corresponding widget from the layout
        widget_to_remove = next(
            widget for widget in self.accounts_list.children if widget.text == txt
        )
        self.accounts_list.remove_widget(widget_to_remove)
        self.data_manager.remove_account(account=account)
