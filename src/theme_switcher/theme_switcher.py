#!/usr/bin/python3
import os
import shutil
import json
import sys

from gi.overrides import Gio, GLib
from pydbus import SessionBus

from .theme_manager import ThemeManager, DBusNightLightManager

share_path = "{}/../../../../share/theme-switcher/".format(
    os.path.dirname(__file__))


def get_system_theme() -> str:
    with open(share_path + 'config.json') as path_config_file:
        theme_file = share_path + \
            json.load(path_config_file)['filenames']['current_theme_file']

    theme_name = 'Adwaita'
    with open(theme_file, 'r', encoding='utf-8') as theme_name_file:
        theme_name = theme_name_file.readline().strip()

    return theme_name


def initial_setup():
    # get path of current file
    here_path = os.path.dirname(__file__)

    # define the systemd service file to be used
    service_file_content = '\n'.join([
        "[Unit]",
        "Description = Automatic Theme Switcher\n",

        "[Service]",
        "Type = simple",
        "ExecStart = {}/../../../../bin/theme_switcher".format(
            os.path.dirname(__file__)),
        "Restart = on-failure"
    ])

    # load the install config from the config.json file
    with open(share_path + 'config.json') as path_config_file:
        install_config = json.load(path_config_file)
        file_list = install_config['files']
        path_list = install_config['paths']
        file_name_list = install_config['filenames']

        for key in file_list.keys():
            file_list[key] = file_list[key].format(here_path)

        for key in path_list.keys():
            path_list[key] = path_list[key].format(here_path)

    # get the status of initial setup
    with open(file_list['initial_setup_file'], 'r') as initial_setup_data:
        setup_done = initial_setup_data.read().strip()

    if setup_done == '0':

        try:
            # create directory structure for systemd service file and the desktop file
            os.mkdir(path_list['systemd_user_service_path'])
            os.mkdir(path_list['autostart_desktop_file_path'])
        except FileExistsError as e:
            print("File already exists")

        # create the systemd service file with contents defined above
        with open(file_list['service_file'], 'w') as service_file_unit:
            service_file_unit.write(service_file_content)

        # copy the desktop file to its correct location
        shutil.copyfile(
            share_path + file_name_list['desktop_file'], file_list['desktop_file'])

        # remove the original file
        os.remove(share_path + file_name_list['desktop_file'])

        # commit initial setup as done
        with open(file_list['initial_setup_file'], 'w') as initial_setup_data:
            initial_setup_data.write('1')


def main():

    # do initial setup
    if len(sys.argv) >= 2 and sys.argv[1] == '--initial-setup':
        initial_setup()
        sys.exit(0)

    # event loop object
    loop = GLib.MainLoop()

    # get session bus instance
    session_bus = SessionBus()

    # obtain DBus NightLight manager service instance
    dbus_nightlight_manager = DBusNightLightManager(session_bus)
    
    # Set theme in the Theme Manager
    ThemeManager.getInstance().setThemeName(get_system_theme())

    # Apply theme according to the current night light status
    ThemeManager.applyTheme()

    # start event loop with support to exit gracefully using Ctrl-C
    try:
        loop.run()
    except KeyboardInterrupt as e:
        loop.quit()
        print("\nExit by Control C")


if __name__ == '__main__':
    main()
