"""Module to define the subcategories settings to insert in the settings page of the app."""
import logging
import time

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import (
    IconLeftWidget,
    IconRightWidget,
    MDList,
    OneLineAvatarIconListItem,
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField

from .dialogbox import DialogBuilder

logger = logging.getLogger(__name__)


class SubcategoryWidget:
    """Subcategory widget to add and remove subcategories."""

    def __init__(self, data_manager):
        logger.info("SubcategoryWidget: %s:  __init__", time.time())
        self.data_manager = data_manager
        self.subcategory_list = MDList()
        self.subcategory_dialog = None

    def generate_subcategory_list(self):
        """Generate a list of widgets to hold each subcategory name.

        Returns:
            MDScrollView: list widget with all subcategories.
        """
        logger.info("SubcategoryWidget: %s:  generate_subcategory_list", time.time())
        for subcategory in self.data_manager.sub_categories:
            self.subcategory_list.add_widget(
                self.single_subcategory_list(subcategory=subcategory)
            )

        # add button to add a new subcategory
        self.subcategory_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"),
                text="Add a new subcategory",
                on_release=self.get_subcategory_name,
            )
        )

        return MDScrollView(self.subcategory_list)

    def single_subcategory_list(self, subcategory):
        """Generate a single widget to hold the subcategory name.

        Args:
            subcategory (str): subcategory name.

        Returns:
            OneLineAvatarIconListItem: widget with icon, description and delete button.
        """
        logger.info("SubcategoryWidget: %s:  single_subcategory_list", time.time())
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="bank"),
            IconRightWidget(
                icon="delete",
                on_release=lambda x, item=subcategory: self.delete_subcategory(item),
            ),
            text=subcategory,
            id=subcategory,
        )

    def delete_subcategory(self, subcategory):
        """Remove a subcategory from the list.

        Args:
            subcategory (str): subcategory name.
        """
        logger.info("SubcategoryWidget: %s: delete_subcategory", time.time())
        # Remove the corresponding widget from the layout
        widget_to_remove = next(
            widget
            for widget in self.subcategory_list.children
            if widget.id == subcategory
        )
        self.subcategory_list.remove_widget(widget_to_remove)
        self.data_manager.remove_subcategory(subcategory=subcategory)

    def get_subcategory_name(self, instance):
        """Get a new subcategory name."""
        logger.info("SubcategoryWidget: %s: get_subcategory_name", time.time())
        # initialize new input widget
        text_input = MDTextField(hint_text="Enter a new subcategory")
        text_input.on_text_validate = lambda: self.add_subcategory(
            input_widget=text_input, subcategory=text_input.text
        )
        # remove button
        self.subcategory_list.remove_widget(instance)
        # add text input to collect new account name
        self.subcategory_list.add_widget(text_input)

    def add_subcategory(self, input_widget, subcategory):
        """Add a new subcategory to the list.

        Args:
            input_widget (widget): widget to remove.
            subcategory (str): subcategory name.
        """
        logger.info("SubcategoryWidget: %s: add_subcategory", time.time())
        # remove text input widget (not needed anymore)
        self.subcategory_list.remove_widget(input_widget)
        # add new account to data manager
        self.data_manager.add_subcategory(subcategory=subcategory)
        # add account to list
        self.subcategory_list.add_widget(
            self.single_subcategory_list(subcategory=subcategory)
        )
        # restore button to add new account
        self.subcategory_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"),
                text="Add a new subcategory",
                on_release=self.get_subcategory_name,
            )
        )

    def get_subcategory_dialog(self, instance):  # pylint: disable=W0613
        """Opens Pop-up box with a list of all subcategories."""
        logger.info("SubcategoryWidget: %s:  get_subcategory_dialog", time.time())
        if not self.subcategory_dialog:
            # create dialog button
            self.subcategory_dialog = DialogBuilder().build_confirmation_dialog(
                title="Add new subcategory:",
                content=MDBoxLayout(
                    self.generate_subcategory_list(),
                    orientation="vertical",
                    # spacing="12dp",
                    size_hint_y=None,
                    height="420dp",
                ),
            )

        self.subcategory_dialog.open()
