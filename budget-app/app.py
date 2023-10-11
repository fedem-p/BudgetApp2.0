import datetime
import os
import random

from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    IconLeftWidget,
    IconRightWidget,
    MDList,
    OneLineAvatarIconListItem,
    OneLineIconListItem,
    OneLineListItem,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField

from core.data_manager import DataManager

DATA_PATH = os.path.abspath("./data/")


class MyBudgetApp(MDApp):
    def on_switch_active(self, instance, value):
        if value:
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

    def build_account_page(self):
        self.accounts_list = MDList()

        for account in self.data_manager.accounts:
            txt = f"{account} | Balance: {self.data_manager.get_account_balance(account=account)}$"

            self.accounts_list.add_widget(
                OneLineAvatarIconListItem(IconLeftWidget(icon="bank"), text=txt)
            )
        self.accounts_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"), text="Add a new account",on_release=self.update_account_list
            )
        )

        return MDScrollView(self.accounts_list)

    def update_account_list(self, instance):
        text_input = MDTextField(hint_text="Enter a new account")
        text_input.on_text_validate = lambda: self.add_new_account(text_input, text_input.text)
        self.accounts_list.remove_widget(instance)
        self.accounts_list.add_widget(text_input)

    def add_new_account(self,text_input, text):
        self.accounts_list.remove_widget(text_input)
        self.data_manager.add_account(account=text)
        txt = f"{text} | Balance: {self.data_manager.get_account_balance(account=text)}$"
        self.accounts_list.add_widget(
                OneLineAvatarIconListItem(IconLeftWidget(icon="bank"), text=txt)
            )
        self.accounts_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"), text="Add a new account",on_release=self.update_account_list
            )
        )

    def build_settings(self):
        switch_layout = MDBoxLayout(orientation="horizontal", padding=20, spacing=10)

        label = MDLabel(text="Toggle Switch")
        switch = MDSwitch()
        switch.bind(active=self.on_switch_active)

        switch_layout.add_widget(label)
        switch_layout.add_widget(switch)

        grid_layout = MDGridLayout(cols=1, adaptive_height=True, padding=10, spacing=10)

        grid_layout.add_widget(switch_layout)
        grid_layout.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="github"),
                text="Download data (csv file)",
                on_release=lambda x: print("Downloading data!"),  # TODO
            )
        )
        grid_layout.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="github"),
                text="Upload data (csv file)",
                on_release=lambda x: print("Uploading data!"),  # TODO
            )
        )
        grid_layout.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="github"),
                text="Categories",
                on_release=lambda x: print("Add/Remove Category"),  # TODO
            )
        )
        grid_layout.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="github"),
                text="SubCategories",
                on_release=lambda x: print("Add/Remove SubCategory"),  # TODO
            )
        )

        return grid_layout

    def build_main_screen(self):
        navbar = MDBottomNavigation(
            MDBottomNavigationItem(
                MDLabel(
                    text="Dashboard",
                    halign="center",
                ),
                name="dashboard",
                text="Dashboard",
                icon="chart-pie",
            ),
            MDBottomNavigationItem(
                self.build_account_page(),
                name="accounts",
                text="Accounts",
                icon="bank",
                badge_icon="numeric-3",
            ),
            MDBottomNavigationItem(
                self.build_transactions(),
                name="transactions",
                text="Transactions",
                icon="format-list-bulleted",
            ),
            MDBottomNavigationItem(
                self.build_settings(),
                name="settings",
                text="Settings",
                icon="cog",
            ),
            selected_color_background="orange",
            text_color_active="lightgrey",
        )

        return MDScreen(
            navbar,
            MDFloatingActionButton(
                icon="plus",
                # TODO: put them in the bottom left corner symmetrically (based on window size)
                pos=(0, navbar.height + 5),
                pos_hint={"right": 0.99},
            ),
        )

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.material_style = "M3"

        self.data_manager = DataManager(data_folder=DATA_PATH)

        self.data_manager.initialize_data()

        return self.build_main_screen()

    def on_start(self):
        # get data

        for transaction in self.data_manager.transactions:
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

    def build_transactions(self):
        self.transaction_list = MDList(id="container")

        return MDScrollView(self.transaction_list)


if __name__ == "__main__":
    MyBudgetApp().run()