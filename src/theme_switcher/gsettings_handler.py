from gi.overrides import Gio
from .themedb import Theme


class GSettingsHandler(object):

    def __init__(self):
        self._desktop_schema = Gio.Settings(schema='org.gnome.desktop.interface')
        self._shell_schema = Gio.Settings(schema='org.gnome.shell.extensions.user-theme')
        
    def applyTheme(self, theme_obj: Theme):
        self._desktop_schema.set_string('gtk-theme', theme_obj['gtk-theme'])
        self._desktop_schema.set_string('icon-theme', theme_obj['icon-theme'])
        self._desktop_schema.set_string('cursor-theme', theme_obj['cursor-theme'])
        self._shell_schema.set_string('name', theme_obj['name'])
