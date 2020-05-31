from .themedb import Theme
from .gsettings_handler import GSettingsHandler
from pydbus import SessionBus


class DBusNightLightManager(object):
    _dbus_color_service = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if DBusNightLightManager._instance is None:
            DBusNightLightManager._instance = super().__new__(cls)
        return DBusNightLightManager._instance

    def __init__(self, bus_instance):
        if DBusNightLightManager._dbus_color_service is None:
            DBusNightLightManager._dbus_color_service = bus_instance.get('org.gnome.SettingsDaemon.Color', '/org/gnome/SettingsDaemon/Color')
            DBusNightLightManager._dbus_color_service.onPropertiesChanged = DBusNightLightManager.processNightLightInvocation

    @staticmethod
    def create(bus_instance: SessionBus) -> None:
        if DBusNightLightManager._instance is None:
            DBusNightLightManager(bus_instance)

    @staticmethod
    def isNightLightEnabled() -> bool:
        return DBusNightLightManager._dbus_color_service.NightLightActive

    @staticmethod
    def processNightLightInvocation(*args) -> None:
        nightlight_status = None
        try:
            nightlight_status = args[1].get('NightLightActive')
        except KeyError as e:
            print("Key 'NightLightActive' not found\n", e)

        if nightlight_status is not None:
            ThemeManager.applyTheme()

    @staticmethod
    def getInstance():
        return DBusNightLightManager._instance

    
class ThemeManager(object):
    _theme_name = None
    _instance = None

    def __new__(cls, *args, **kwargs):
        if ThemeManager._instance is None:
            ThemeManager._instance = super().__new__(cls)
        return ThemeManager._instance

    def __init__(self, theme_name=None):
        if ThemeManager._theme_name is None:
            if theme_name is None or theme_name not in Theme.getList():
                ThemeManager._theme_name = 'Adwaita'
            else:
                ThemeManager._theme_name = theme_name

    @staticmethod
    def getInstance():
        return ThemeManager._instance

    @staticmethod
    def getCurrentTheme():
        night_light_status = 1 if DBusNightLightManager.isNightLightEnabled() is True else 0
        return Theme(ThemeManager.getThemeName()).getThemeVariants()[night_light_status]

    @staticmethod
    def setThemeName(theme_name: str):
        if theme_name is None or theme_name not in Theme.getList():
            ThemeManager._theme_name = 'Adwaita'
        else:
            ThemeManager._theme_name = theme_name

    @staticmethod
    def getThemeName() -> str:
        return ThemeManager._theme_name

    @staticmethod
    def applyTheme() -> None:

        theme = ThemeManager.getCurrentTheme()
        gnome_theme_handler = GSettingsHandler()
        gnome_theme_handler.applyTheme(theme)
        
