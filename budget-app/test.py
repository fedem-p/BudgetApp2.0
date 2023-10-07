from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "A200"

        main_screen = BoxLayout(orientation="vertical")
        open_settings_button = MDRaisedButton(
            text="Open Settings", on_release=self.open_settings
        )
        main_screen.add_widget(open_settings_button)
        return main_screen

    def open_settings(self, instance):
        settings_screen = MDScreen()

        settings_content = BoxLayout(orientation="vertical")

        # Create settings options using KivyMD components
        setting_option_1 = MDLabel(text="Setting Option 1")
        setting_option_2 = MDLabel(text="Setting Option 2")

        settings_content.add_widget(setting_option_1)
        settings_content.add_widget(setting_option_2)

        settings_screen.add_widget(settings_content)

        close_settings_button = MDRaisedButton(
            text="Close Settings", on_release=self.close_settings
        )

        settings_screen.add_widget(close_settings_button)
        self.root.add_widget(settings_screen)

    def close_settings(self, instance):
        for child in self.root.children:
            if isinstance(child, MDScreen):
                self.root.remove_widget(child)


if __name__ == "__main__":
    MainApp().run()
