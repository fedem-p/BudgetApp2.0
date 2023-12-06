"""Module to build a dialog box with an input plus a cancel and save button."""
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog


class DialogBuilder:  # pylint: disable=too-few-public-methods
    """Builder class for a dialog box."""

    def __init__(self):
        """initialize widget to return to None."""
        self.widget = None

    def build_dialog(self, content, title, on_release_function, widget_type="custom"):
        """Builds and returns a dialog box based on the inputs with a save and cancel button.

        Args:
            content (MDwidget): Any widget that can take an input.
            title (str): Title of the dialog box.
            on_release_function (function): function to call when save button is pressed.
                        It will always pass the content widget as input to the function.
            widget_type (str, optional): type of the dialog box. Defaults to "custom".

        Returns:
            MDDialog: dialog box.
        """
        self.widget = MDDialog(
            title=title,
            content_cls=content,
            type=widget_type,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self.widget.dismiss()),
                MDFlatButton(
                    text="Save",
                    on_release=lambda x, item=content: on_release_function(item),
                ),
            ],
        )

        return self.widget
