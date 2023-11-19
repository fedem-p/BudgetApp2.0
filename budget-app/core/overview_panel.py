"""Module to define the overview page to insert in the bottom navbar of the app."""
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.label import MDLabel

from .data_manager import DataManager


class OverviewPage:
    """
    Class to define the App page that holds an overview of
    transactions and accounts balances.
    """

    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def build_page(self):
        """Builds a page using a bottom navbar item and
        calls a function to generate the content of the page.

        Returns:
            MDBottomNavigationItem: Bottom navbar item.
        """
        return MDBottomNavigationItem(
            self.generate_overview(),
            name="dashboard",
            text="Dashboard",
            icon="chart-pie",
        )

    def generate_overview(self):
        """Generates the overview page content.

        Returns:
            MDLabel: page content
        """
        return MDLabel(
            text="Dashboard",
            halign="center",
        )
