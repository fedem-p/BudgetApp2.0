"""Module to define the overview page to insert in the bottom navbar of the app."""
import logging
import time

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.label import MDLabel

from .data_manager import DataManager

logger = logging.getLogger(__name__)


class OverviewPage:
    """
    Class to define the App page that holds an overview of
    transactions and accounts balances.
    """

    def __init__(self, data_manager: DataManager):
        logger.info("OverviewPage: %s:  __init__", time.time())
        self.data_manager = data_manager

    def build_page(self):
        """Builds a page using a bottom navbar item and
        calls a function to generate the content of the page.

        Returns:
            MDBottomNavigationItem: Bottom navbar item.
        """
        logger.info("OverviewPage: %s:  build_page", time.time())
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
        logger.info("OverviewPage: %s:  generate_overview", time.time())
        return MDLabel(
            text="Dashboard",
            halign="center",
        )
