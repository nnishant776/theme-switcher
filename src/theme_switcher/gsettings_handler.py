from gi.overrides import Gio
from .themedb import Theme


class GSettingsHandler(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if GSettingsHandler._instance is None:
            GSettingsHandler._instance = super().__new__(cls)
            GSettingsHandler._instance.desktop_schema = None
            GSettingsHandler._instance.shell_schema = None
        return GSettingsHandler._instance

    def __init__(self):
        if GSettingsHandler._instance is None:
            GSettingsHandler._instance = self
        if self.desktop_schema is None:
            self.desktop_schema = Gio.Settings(
                schema='org.gnome.desktop.interface')
        if self.shell_schema is None:
            self.shell_schema = Gio.Settings(
                schema='org.gnome.shell.extensions.user-theme')

    @staticmethod
    def getInstance():
        if GSettingsHandler._instance is None:
            GSettingsHandler()

        return GSettingsHandler._instance

    def applySchema(self, theme_obj: Theme):
        self.desktop_schema.set_string('gtk-theme', theme_obj['gtk-theme'])
        self.desktop_schema.set_string('icon-theme', theme_obj['icon-theme'])
        self.desktop_schema.set_string(
            'cursor-theme', theme_obj['cursor-theme'])
        self.shell_schema.set_string('name', theme_obj['name'])
