# modorganizer-game_generic
This repository retains a Mod Organizer 2 pluging to manage a generic folder, as well as modifications of this plugin to support specific games.

## Description:
    game_generic.py is a MO2 plugin that allows users to install mods in an arbitrary location.
    This is a suboptimal solution with obvious compromises such as orphaned ui elements of
    features that are missing like the empty plugins tab and possible bugs.
    
    There are also inherent limitations to which files can be virtualized, derived from the MO2 VFS. 
    Specifically load-time linked dlls such as d3dx9_42.dll will not get properly virtualized to programs
    as those are loaded before the Virtual Library dll can be loaded (one of the reasons for which Mo2 
    does not support mods that install in the game directory as most of those are dlls).
    
    In this repo also contains a collection of specific game_plugins adaptd from the generic version.
    
## Installation:
    Drop game_generic.py inside the MO2 Plugins folder, located inside the MO2 install directory.
    
    Do the same for a game specific version.

## Usage:
    Open MO2, create a new instance and choose a name for it. Mo2 will then ask you to 
    either select a game from the list of detected ones or browse to a game directory.
    Select the Browse option and choose the folder in which you want Mo2 to put the mod files.
    A new generic instance will be generated.
    Attention! If this plugin is installed you might accidentally create a generic instance 
    instead of one of another supported game. It's advised to not have this plugin installed
    when creating instances for actually supported games.

    For the game specific versions, some will offer auto detection and others will require to select the game folder.
    For more information please check the description contained in the files themselves.
    
## Supporting a specific game:
    By editing some of the contents of this plugin, it can be adapted to rudimentarily support 
    a specific game in better capacity than just defining a target folder.
    All the required fields to be filled have been commented to help understand what they 
    are meant to do. You can check the very well made Qt online documentation for Qt types used.
    
    This file is released under MIT license so feel free to adapt it to a specific game
    and distribute it.
    
    If you are looking to add support for a game we would be happy to discuss it with you
    at the MO2 Development Discord server: https://discord.gg/5tCqt6V .
