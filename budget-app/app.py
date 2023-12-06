"""Budget app to track expenses and income."""
import os

from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.screen import MDScreen

from core.account_panel import AccountPage
from core.data_manager import DataManager
from core.overview_panel import OverviewPage
from core.settings_panel import SettingsPage
from core.transactions_panel import TransactionPage

DATA_PATH = os.path.abspath("./data/")


class MyBudgetApp(MDApp):
    """Creates an app to track expenses and income."""

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.material_style = "M2"

        self.data_manager = DataManager(data_folder=DATA_PATH)  # pylint: disable=W0201

        self.data_manager.initialize_data()

        self.account_page = AccountPage(  # pylint: disable=W0201
            data_manager=self.data_manager
        )
        self.transaction_page = TransactionPage(  # pylint: disable=W0201
            data_manager=self.data_manager
        )
        self.overview_page = OverviewPage(  # pylint: disable=W0201
            data_manager=self.data_manager
        )
        self.settings_page = SettingsPage(  # pylint: disable=W0201
            data_manager=self.data_manager
        )

        return self.build_main_screen()

    def build_main_screen(self):
        """Function to create the main screen of the app.

        Returns:
            MDScreen: screen with a bottom navbar and multiple pages.
        """
        navbar = MDBottomNavigation(
            self.overview_page.build_page(),
            self.account_page.build_page(),
            self.transaction_page.build_page(),
            self.settings_page.build_page(),
            selected_color_background="orange",
            text_color_active="lightgrey",
        )

        return MDScreen(navbar)


if __name__ == "__main__":
    MyBudgetApp().run()
