"""Module to define the categories settings to insert in the settings page of the app."""
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


class CategoryWidget:
    """Category widget to add and remove categories."""

    def __init__(self, data_manager):
        logger.info("CategoryWidget: %s:  __init__", time.time())
        self.data_manager = data_manager
        self.category_list = MDList()
        self.category_dialog = None

    def generate_category_list(self):
        """Generate a list of widgets to hold each category name.

        Returns:
            MDScrollView: list widget with all categories.
        """
        logger.info("CategoryWidget: %s:  generate_category_list", time.time())
        for category in self.data_manager.categories:
            self.category_list.add_widget(self.single_category_list(category=category))

        # add button to add a new category
        self.category_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"),
                text="Add a new category",
                on_release=self.get_category_name,
            )
        )

        return MDScrollView(self.category_list)

    def single_category_list(self, category):
        """Generate a single widget to hold the category name.

        Args:
            category (str): category name.

        Returns:
            OneLineAvatarIconListItem: widget with icon, description and delete button.
        """
        logger.info("CategoryWidget: %s:  single_category_list", time.time())
        return OneLineAvatarIconListItem(
            IconLeftWidget(icon="bank"),
            IconRightWidget(
                icon="delete",
                on_release=lambda x, item=category: self.delete_category(item),
            ),
            text=category,
            id=category,
        )

    def delete_category(self, category):
        """Remove a category from the list.

        Args:
            category (str): category name.
        """
        logger.info("CategoryWidget: %s: delete_category", time.time())
        # Remove the corresponding widget from the layout
        widget_to_remove = next(
            widget for widget in self.category_list.children if widget.id == category
        )
        self.category_list.remove_widget(widget_to_remove)
        self.data_manager.remove_category(category=category)

    def get_category_name(self, instance):
        """Get a new category name."""

        logger.info("CategoryWidget: %s:  get_category_name", time.time())
        # initialize new input widget
        text_input = MDTextField(hint_text="Enter a new category")
        text_input.on_text_validate = lambda: self.add_category(
            input_widget=text_input, category=text_input.text
        )
        # remove button
        self.category_list.remove_widget(instance)
        # add text input to collect new account name
        self.category_list.add_widget(text_input)

    def add_category(self, input_widget, category):
        """Add a new category to the list.

        Args:
            input_widget (widget): widget to remove.
            category (str): category name.
        """
        logger.info("CategoryWidget: %s:  add_category", time.time())
        # remove text input widget (not needed anymore)
        self.category_list.remove_widget(input_widget)
        # add new account to data manager
        self.data_manager.add_category(category=category)
        # add account to list
        self.category_list.add_widget(self.single_category_list(category=category))
        # restore button to add new account
        self.category_list.add_widget(
            OneLineAvatarIconListItem(
                IconLeftWidget(icon="plus"),
                text="Add a new category",
                on_release=self.get_category_name,
            )
        )

    def get_category_dialog(self, instance):  # pylint: disable=W0613
        """Opens Pop-up box with a list of all categories."""
        logger.info("CategoryWidget: %s:  get_category_dialog", time.time())
        if not self.category_dialog:
            # create dialog button
            self.category_dialog = DialogBuilder().build_dialog(
                title="Add new Category:",
                content=MDBoxLayout(
                    self.generate_category_list(),
                    orientation="vertical",
                    # spacing="12dp",
                    size_hint_y=None,
                    height="420dp",
                ),
            )

        self.category_dialog.open()
