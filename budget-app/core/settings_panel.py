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

from .data_manager import DataManager


class SettingsPage:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def build_page(self):
        return MDBottomNavigationItem(
            self.build_settings(),
            name="settings",
            text="Settings",
            icon="cog",
        )

    def on_switch_active(self, instance, value):
        pass
        # if value:
        #     self.theme_cls.theme_style = "Light"
        # else:
        #     self.theme_cls.theme_style = "Dark"

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
