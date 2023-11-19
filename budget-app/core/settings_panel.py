"""Module to define the settings page to insert in the bottom navbar of the app."""
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import IconLeftWidget, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDSwitch

from .data_manager import DataManager


class SettingsPage:
    """
    Class to define the App page that holds all the settings
    and any functionality related to them.
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
            self.build_settings(),
            name="settings",
            text="Settings",
            icon="cog",
        )

    def on_switch_active(self, instance, value):
        """Upon change in the switch selection
        changes the color of the app theme.

        Args:
            instance (_type_): TODO
            value (_type_): TODO
        """
        pass  # pylint: disable=W0107
        # if value:
        #     self.theme_cls.theme_style = "Light"
        # else:
        #     self.theme_cls.theme_style = "Dark"

    def build_settings(self):
        """Generates the settings page content.

        Returns:
            MDGridLayout: settings page content
        """
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
                on_release=lambda x: print(
                    "Downloading data!"
                ),  # TODO # pylint: disable=W0511
            )
        )
        grid_layout.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="github"),
                text="Upload data (csv file)",
                on_release=lambda x: print(
                    "Uploading data!"
                ),  # TODO # pylint: disable=W0511
            )
        )
        grid_layout.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="github"),
                text="Categories",
                on_release=lambda x: print(
                    "Add/Remove Category"
                ),  # TODO # pylint: disable=W0511
            )
        )
        grid_layout.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="github"),
                text="SubCategories",
                on_release=lambda x: print(
                    "Add/Remove SubCategory"
                ),  # TODO # pylint: disable=W0511
            )
        )

        return grid_layout
