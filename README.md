# TouchPortal-Windows-Shortcut

- [TouchPortal-Windows-Shortcut](#TouchPortal-Windows-Shortcut)
  - [What is this](#What-is-this?) 
  - [Fonctionality](#Fonctionality)
    - [States](#States)
    - [Settings](#Settings)
  - [Installing](#Installing)
  - [Bugs and Support](#bugs-and-suggestion)

# What is this?

TouchPortal-Windows-Shortcut plugin is a solution for easily retrieving the path to an application or shortcut, and the associated icon. 

# Fonctionality

## Action

## State
- [State] [Shortcut] Path of the shortcut icon 0 *TP.Plugins.win_shortcut.states.shortcut_icon_0*
- [State] [Shortcut] Path of the shortcut icon 1 *TP.Plugins.win_shortcut.states.shortcut_icon_1*
- [State] [Shortcut] Path of the shortcut icon 3 *TP.Plugins.win_shortcut.states.shortcut_icon_2*
- [State] [Shortcut] Path of the shortcut icon 3 *TP.Plugins.win_shortcut.states.shortcut_icon_3*
- [State] [Shortcut] Path of the shortcut icon 4 *TP.Plugins.win_shortcut.states.shortcut_icon_4*
- [State] [Shortcut] Path of the shortcut icon 5 *TP.Plugins.win_shortcut.states.shortcut_icon_5*
- [State] [Shortcut] Path of the shortcut 0 *TP.Plugins.win_shortcut.states.shortcut_path_0*
- [State] [Shortcut] Path of the shortcut 1 *TP.Plugins.win_shortcut.states.shortcut_path_1*
- [State] [Shortcut] Path of the shortcut 2 *TP.Plugins.win_shortcut.states.shortcut_path_2*
- [State] [Shortcut] Path of the shortcut 3 *TP.Plugins.win_shortcut.states.shortcut_path_3*
- [State] [Shortcut] Path of the shortcut 4 *TP.Plugins.win_shortcut.states.shortcut_path_4*
- [State] [Shortcut] Path of the shortcut 5 *TP.Plugins.win_shortcut.states.shortcut_path_5*

## Settings

There are currently 1 settings for this plugin

* `Shortcut directory` - The path of the file where your shortcuts are located
    * Default: $HOME/Desktop/
    * Valid Values: A directory path.

# Installing

### Step 1: Download Plugin
Download the Touch Portal plugin from the [Releases]() section of this repository.

### Step 2: Import into Touch Portal
Select the Gear icon at the top of Touch Portal desktop window and select `Import plug-in...`.

### Step 3: Locate .tpp and Open
Navigate to where you downloaded the .tpp file from Step 1, select it and click "Open".

### Step 4: Select `Trust Always` on Warning Popup

In order for this plugin to run when you start Touch Portal, you will need to select `Trust Always` on the popup that appears, if you do not do this, it will show up every time you start Touch Portal.

### Step 5: Click `OK` on Popup

Once you trust the plugin, click `OK` button.

### Step 6: Set parameters and restart Touch Portal

After importing the plugin, go to settings and set the values for `Shortcut directory` and `Icon directory` (See the [Settings](#Settings) section for more information on how to modify these parameters.). Once configured, restart Touch Portal. 

# Bugs/Enhancements

Open an issue on github or join offical [TouchPortal Discord](https://discord.gg/touchportal) for support.
