import datetime
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
from core.data_manager import DataManager
import os

DATA_PATH = os.path.abspath("./data/")


class MyBudgetApp(MDApp):
    def on_switch_active(self, instance, value):
        if value:
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

    def build_account_page(self):
        x = 13.99

        accounts = MDList()

        for account in self.data_manager.accounts:

            txt = f"{account} | Balance: {self.data_manager.get_account_balance(account=account)}$" 

            accounts.add_widget(
                OneLineAvatarIconListItem(IconLeftWidget(icon="bank"), text=txt)
            )
        accounts.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"), text="Add a new account"
            )
        )

        return MDScrollView(accounts)

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


# from kivy.lang import Builder
# from kivy.properties import StringProperty
# from kivy.uix.screenmanager import Screen

# from kivymd.icon_definitions import md_icons
# from kivymd.app import MDApp
# from kivymd.uix.list import OneLineIconListItem


# Builder.load_string(
#     '''
# #:import images_path kivymd.images_path


# <CustomOneLineIconListItem>

#     IconLeftWidget:
#         icon: root.icon


# <PreviousMDIcons>

#     MDBoxLayout:
#         orientation: 'vertical'
#         spacing: dp(10)
#         padding: dp(20)

#         MDBoxLayout:
#             adaptive_height: True

#             MDIconButton:
#                 icon: 'magnify'

#             MDTextField:
#                 id: search_field
#                 hint_text: 'Search icon'
#                 on_text: root.set_list_md_icons(self.text, True)

#         RecycleView:
#             id: rv
#             key_viewclass: 'viewclass'
#             key_size: 'height'

#             RecycleBoxLayout:
#                 padding: dp(10)
#                 default_size: None, dp(48)
#                 default_size_hint: 1, None
#                 size_hint_y: None
#                 height: self.minimum_height
#                 orientation: 'vertical'
# '''
# )


# class CustomOneLineIconListItem(OneLineIconListItem):
#     icon = StringProperty()


# class PreviousMDIcons(Screen):

#     def set_list_md_icons(self, text="", search=False):
#         '''Builds a list of icons for the screen MDIcons.'''

#         def add_icon_item(name_icon):
#             self.ids.rv.data.append(
#                 {
#                     "viewclass": "CustomOneLineIconListItem",
#                     "icon": name_icon,
#                     "text": name_icon,
#                     "callback": lambda x: x,
#                 }
#             )

#         self.ids.rv.data = []
#         for name_icon in md_icons.keys():
#             if search:
#                 if text in name_icon:
#                     add_icon_item(name_icon)
#             else:
#                 add_icon_item(name_icon)


# class MainApp(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.screen = PreviousMDIcons()

#     def build(self):
#         return self.screen

#     def on_start(self):
#         self.screen.set_list_md_icons()


# MainApp().run()
