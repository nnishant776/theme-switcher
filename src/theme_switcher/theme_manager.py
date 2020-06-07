from .themedb import Theme
from .gsettings_handler import GSettingsHandler
from pydbus import SessionBus


class DBusNightLightManager(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if DBusNightLightManager._instance is None:
            DBusNightLightManager._instance = super().__new__(cls)
            DBusNightLightManager._instance.dbus_color_service = None
        return DBusNightLightManager._instance

    def __init__(self, bus_instance=None):
        if DBusNightLightManager._instance is None:
            DBusNightLightManager._instance = self
        if self.dbus_color_service is None:
            if bus_instance is None:
                bus_instance = SessionBus()
            self.dbus_color_service = bus_instance.get(
                'org.gnome.SettingsDaemon.Color', '/org/gnome/SettingsDaemon/Color')
            self.dbus_color_service.onPropertiesChanged = self.processNightLightInvocation

    @staticmethod
    def getInstance() -> None:
        if DBusNightLightManager._instance is None:
            DBusNightLightManager()

        return DBusNightLightManager._instance

    def isNightLightEnabled(self) -> bool:
        return self.dbus_color_service.NightLightActive

    def processNightLightInvocation(self, *args) -> None:
        nightlight_status = None
        try:
            nightlight_status = args[1].get('NightLightActive')
        except KeyError as e:
            print("Key 'NightLightActive' not found\n")

        if nightlight_status is not None:
            ThemeManager.applyTheme()


class ThemeManager(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if ThemeManager._instance is None:
            ThemeManager._instance = super().__new__(cls)
            ThemeManager._instance.theme_name = None
            ThemeManager._instance.gsettings_handler = None
        return ThemeManager._instance

    def __init__(self, theme_name=None):
        if ThemeManager._instance is None:
            ThemeManager._instance = self
        if theme_name is None or theme_name not in Theme.getList():
            if self.theme_name is None:
                self.theme_name = 'Adwaita'
        else:
            self.theme_name = theme_name

        if self.gsettings_handler is None:
            self.gsettings_handler = GSettingsHandler()

    @staticmethod
    def getInstance():
        if ThemeManager._instance is None:
            ThemeManager()
            
        return ThemeManager._instance

    def getCurrentTheme(self):
        night_light_status = 1 if DBusNightLightManager.getInstance(
        ).isNightLightEnabled() is True else 0
        return Theme(self.getThemeName()).getThemeVariants()[night_light_status]

    def setThemeName(self, theme_name: str):
        if theme_name is None or theme_name not in Theme.getList():
            if self.theme_name is None:
                self.theme_name = 'Adwaita'
        else:
            self.theme_name = theme_name

    def getThemeName(self) -> str:
        return self.theme_name

    @staticmethod
    def applyTheme() -> None:
        theme = ThemeManager.getInstance().getCurrentTheme()
        gnome_theme_handler = GSettingsHandler()
        gnome_theme_handler.applySchema(theme)
