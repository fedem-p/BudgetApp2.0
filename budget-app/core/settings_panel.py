"""Module to define the settings page to insert in the bottom navbar of the app."""
import logging
import time

from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import IconLeftWidget, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDSwitch

from .data_manager import DataManager
from .utils.category_settings import CategoryWidget
from .utils.subcategory_settings import SubcategoryWidget

logger = logging.getLogger(__name__)


class SettingsPage:
    """
    Class to define the App page that holds all the settings
    and any functionality related to them.
    """

    def __init__(self, data_manager: DataManager):
        logger.info("SettingsPage: %s:  __init__", time.time())
        self.data_manager = data_manager
        self.category_settings = CategoryWidget(self.data_manager)
        self.subcategory_settings = SubcategoryWidget(self.data_manager)

    def build_page(self):
        """Builds a page using a bottom navbar item and
        calls a function to generate the content of the page.

        Returns:
            MDBottomNavigationItem: Bottom navbar item.
        """
        logger.info("SettingsPage: %s:  build_page", time.time())
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
        logger.info("SettingsPage: %s:  build_settings", time.time())
        switch_layout = MDBoxLayout(orientation="horizontal", padding=20, spacing=10)

        label = MDLabel(text="Toggle Switch")
        switch = MDSwitch()
        switch.bind(active=self.on_switch_active)

        switch_layout.add_widget(label)
        switch_layout.add_widget(switch)

        grid_layout = MDGridLayout(cols=1, adaptive_height=True, padding=10, spacing=10)

        grid_layout.add_widget(switch_layout)
        grid_layout.add_widget(self.get_download_button())
        grid_layout.add_widget(self.get_upload_button())
        grid_layout.add_widget(self.get_category_settings())
        grid_layout.add_widget(self.get_subcategory_settings())

        return grid_layout

    def get_download_button(self):
        """Returns a one line settings button to download the data.

        Returns:
            OneLineAvatarIconListItem: Settings button.
        """
        logger.info("SettingsPage: %s:  get_download_button", time.time())
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="github"),
            text="Download data (csv file)",
            on_release=lambda x: print(
                "Downloading data!"
            ),  # TODO # pylint: disable=W0511
        )

    def get_upload_button(self):
        """Returns a one line settings button to upload data.

        Returns:
            OneLineAvatarIconListItem: Settings button.
        """
        logger.info("SettingsPage: %s:  get_upload_button", time.time())
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="github"),
            text="Upload data (csv file)",
            on_release=lambda x: print(
                "Uploading data!"
            ),  # TODO # pylint: disable=W0511
        )

    def get_category_settings(self):
        """Returns a one line settings button to add/remove categories.

        Returns:
            OneLineAvatarIconListItem: Settings button.
        """
        logger.info("SettingsPage: %s:  get_category_settings", time.time())
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="github"),
            text="Categories",
            on_release=self.category_settings.get_category_dialog,
        )

    def get_subcategory_settings(self):
        """Returns a one line settings button to add/remove subcategories.

        Returns:
            OneLineAvatarIconListItem: Settings button.
        """
        logger.info("SettingsPage: %s:  get_subcategory_settings", time.time())
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="github"),
            text="SubCategories",
            on_release=self.subcategory_settings.get_subcategory_dialog,
        )
