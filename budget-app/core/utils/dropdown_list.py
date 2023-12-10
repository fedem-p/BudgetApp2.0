"""Module to build a dropdown list menu."""
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu


class DropdownBuilder:
    """Builds a drop down menu from a list of items."""

    def __init__(  # pylint: disable=R0913
        self,
        items,
        main_id=None,
        initial_text=None,
        pos_hint=None,
        size=None,
    ):
        pos_hint = {"center_x": 0.5, "center_y": 0.5} if pos_hint is None else pos_hint
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": item,
                "on_release": lambda x=item: self.set_item(x),
            }
            for item in items
        ]
        self.menu = MDDropdownMenu(
            caller=None,
            items=self.menu_items,
            position="center",
            width_mult=4,
        )
        if size is None:
            self.drop_item = OneLineListItem(
                id=items[0] if main_id is None else main_id,
                text=items[0] if initial_text is None else initial_text,
                on_release=lambda x: self.menu.open(),
            )
        else:
            self.drop_item = OneLineListItem(
                id=items[0] if main_id is None else main_id,
                text=items[0] if initial_text is None else initial_text,
                on_release=lambda x: self.menu.open(),
                size_hint=(None, None),
                pos_hint=pos_hint,
                width=size[0],
                height=size[1],
            )

        self.menu.caller = self.drop_item

    def set_item(self, text_item):
        """Sets the current selected item.

        Args:
            text_item (str): String value from the selected item.
        """
        self.drop_item.text = text_item
        self.menu.dismiss()

    def get_dropdown_list(self):
        """Returns the dropdown widget.

        Returns:
            OneLineListItem: Widget that opens a dropdown menu when clicked.
        """
        return self.drop_item

    def get_selected_item(self):
        """Returns currently selected text.

        Returns:
            str: text of the currently selected item.
        """
        return self.drop_item.text
