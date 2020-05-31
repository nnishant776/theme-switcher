# Automatic Theme Switcher
A program to switch between light and dark themes based on current night light status. This program has been written and designed predominantly for GNOME Desktop Environment but could be extended to other DE.

----
## Getting started

To install and run this program, you need to have  at least [Python 3](http://www.python.org) (version 3.5 or later) and Pip installed on your system. Then you can simply download the file in dist folder with .whl extension, navigate to the dowload directory and run the below command.

    pip3 install theme_switcher-0.1-py3-none-any.whl



The program will run automatically at startup after user login once configured.

----
## Configuration
After the installation, a bash script file named theme_manager will be present in `$HOME/.local/bin` directory. The help output for this script is shown below.


    $ theme_manager --help

    Usage: 

    theme_manager --help  Display this help print

    theme_manager --initial-setup  Do initial setup before activating theme switcher

    theme_manager --set-theme THEME  Set the one of the themes listed in the themes.json

    theme_manager --uninstall  Uninstall the theme switcher

    theme_manager --edit-themes  Edit/Add to the list of themes and its variants known to the program

To configure, first run

`theme_manager --initial-setup`

This will configure the program for autostart and install a systemd service file as mentioned above.

----
## Usage

By default, the program is configured to use the Adwaita's light and dark theme variants. To use your own theme, you can define the light and dark sets of the said theme in `$HOME/.local/share/theme-switcher/config.json` file, either manually or by using `theme_manager --edit-themes`. This command will open `config.json` file in your preferred editor, if one is set in environment, otherwise it will open the file using `vi`.

If your theme is already defined in `config.json`, then you can directly set the theme using `theme_manager --set-theme THEME_NAME`. Make sure both light and dark variants of the theme are defined, otherwise it won't work. When the theme is set, it will automatically switch between the light and dark variants according to night light status (if enabled).

----
## Defining themes

Below is a sample definition of a theme


    {
        "Adwaita": [
            {
                "gtk-theme": "Adwaita",
                "icon-theme": "Adwaita",
                "cursor-theme": "Adwaita",
                "name": ""
            },
            {
                "gtk-theme": "Adwaita-dark",
                "icon-theme": "Adwaita",
                "cursor-theme": "Adwaita",
                "name": ""
            }
        ]
    }


Below is an explanation of the fields:

* **gtk-theme** : The name of GTK application theme which decoreates the windows and controls
* **icon-theme** : The name of icon theme, e.g., Breeze, Adwaita, Yaru, etc..
* **cursor-theme** : The name of cursor theme, if you are using something other than the default.
* **name** : The name of the GNOME Shell theme that you wish to use.

The first set of the above entries in the theme specification is are the values used for the 'light' variant of the theme and the next for the 'dark' variant.












