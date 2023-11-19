import os

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

from core.account_panel import AccountPage
from core.data_manager import DataManager
from core.overview_panel import OverviewPage
from core.settings_panel import SettingsPage
from core.transactions_panel import TransactionPage

DATA_PATH = os.path.abspath("./data/")


class MyBudgetApp(MDApp):
    def build_main_screen(self):
        navbar = MDBottomNavigation(
            self.overview_page.build_page(),
            self.account_page.build_page(),
            self.transaction_page.build_page(),
            self.settings_page.build_page(),
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

        self.account_page = AccountPage(data_manager=self.data_manager)
        self.transaction_page = TransactionPage(data_manager=self.data_manager)
        self.overview_page = OverviewPage(data_manager=self.data_manager)
        self.settings_page = SettingsPage(data_manager=self.data_manager)

        return self.build_main_screen()


if __name__ == "__main__":
    MyBudgetApp().run()
