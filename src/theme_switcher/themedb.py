import json
import os

class Theme(object):

    _theme_collection = json.load(open("{}/../../../../share/theme-switcher/themes.json".format(os.path.dirname(__file__)),'r'))

    def __init__(self, theme_name: str):
        
        self._theme_name = theme_name

    def getThemeVariants(self):
        return Theme._theme_collection[self._theme_name]

    def getLightTheme(self):
        return Theme._theme_collection[self._theme_name][0]

    def getDarkTheme(self):
        return Theme._theme_collection[self._theme_name][1]

    def getThemeName(self) -> str:
        return self._theme_name

    def setThemeName(self, theme_name: str) -> None:
        self._theme_name = theme_name

    @staticmethod
    def getList():
        return Theme._theme_collection.keys()
    
