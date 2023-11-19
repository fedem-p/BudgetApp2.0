from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    IconLeftWidget,
    IconRightWidget,
    MDList,
    OneLineAvatarIconListItem,
    OneLineListItem,
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from .data_manager import DataManager


class OverviewPage:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def build_page(self):
        return MDBottomNavigationItem(
            self.generate_overview(),
            name="dashboard",
            text="Dashboard",
            icon="chart-pie",
        )

    def generate_overview(self):
        return MDLabel(
            text="Dashboard",
            halign="center",
        )
