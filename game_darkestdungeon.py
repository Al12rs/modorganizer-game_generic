"""
MIT License

Copyright (c) 2018 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
## Description:
    This is a MO2 plugin that allows users to install mods in an arbitrary location.
    This is a suboptimal solution with obvious compromises such as orphaned ui elements of
    features that are missing like the empty plugins tab and possible bugs.
    
    There are also inherent limitations to which files can be virtualized, derived from the MO2 VFS. 
    Specifically load-time linked dlls such as d3dx9_42.dll will not get properly virtualized to programs
    as those are loaded before the Virtual Library dll can be loaded (one of the reasons for which Mo2 
    does not support mods that install in the game directory as most of those are dlls).

## Installation:
    Drop game_generic.py inside the MO2 Plugins folder, located inside the MO2 install directory.

## Usage:
    Open MO2, create a new instance and choose a name for it. Mo2 will then ask you to 
    either select a game from the list of detected ones or browse to a game directory.
    Select the Browse option and choose the folder in which you want Mo2 to put the mod files.
    A new generic instance will be generated.

    Attention! If this plugin is installed you might accidentally create a generic instance 
    instead of one of another supported game. It's advised to not have this plugin installed
    when creating instances for actually supported games.

## Supporting a specific game:
    By editing some of the contents of this plugin, it can be adapted to rudimentally support 
    a specific game in better capacity than just defining a target folder.
    All the required fields to be filled have been commented to help understand what they 
    are meant to do. You can check the very well made Qt online documentation for Qt types used.
    
    This file is released under MIT license so feel free to adapt it to a specific game
    and distribute it.
    
    If you are looking to add support for a game we would be happy to discuss it with you
    at the MO2 Development Discord server: https://discord.gg/5tCqt6V .
"""

import sys
import os

from PyQt5.QtCore import QCoreApplication, QDateTime, QDir, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

if "mobase" not in sys.modules:
    import mock_mobase as mobase

class DarkestDungeonGamePlugins(mobase.GamePlugins):
    """
    Game feature class for plugin type mods.
    This is currently required to be implemented or Mo2 will crash.
    """
    def __init__(self, organizer):
        super(DarkestDungeonGamePlugins, self).__init__()
        self.__organizer = organizer
        self.__lastRead = None
    
    def writePluginLists(self, pluginList):
        return
    
    def readPluginLists(self, pluginList):
        return
    
    def lightPluginsAreSupported(self):
        return False

    def getLoadOrder(self, loadOrder):
        return

class DarkestDungeon(mobase.IPluginGame):
    """
    Actual plugin class, extends the IPluginGame interface, meaning it adds support for a new game.
    """

    def __init__(self):
        super(DarkestDungeon, self).__init__()
        self.__featureMap = {}

    """
    Here IPlugin interface stuff. 
    """
    
    def init(self, organizer):
        self.__featureMap[mobase.GamePlugins] = DarkestDungeonGamePlugins(organizer)
        self.m_GameDir=QDir()
        self.m_DataDir=QDir()
        self.m_DocumentsDir=QDir()
        return True

    def name(self):
        """
        @return name of this plugin (used for example in the settings menu).
        @note Please ensure you use a name that will not change. Do NOT include a version number in the name.
        Do NOT use a localizable string (tr()) here.
        Settings for example are tied to this name, if you rename your plugin you lose settings users made.
        """
        return "Darkest Dungeon Plugin"

    def author(self):
        """
        @return author of this plugin.
        AnyOldName3 for initial fake game mock implementation,
        AL12 for generic game support and documentation comments,
        erri120 for adaption to Darkest Dungeon
        """
        return "AnyOldName3, AL12, erri120"

    def description(self):
        """
        @return a short description of the plugin to be displayed to the user
        """
        return self.__tr("Adds support for Darkest Dungeon. Based on the GenericGamePlugin by AnyOldName3 and AL12 version 0.1.0")

    def version(self):
        """
        @return version of the plugin. This can be used to detect outdated versions of plugins.
        """
        return mobase.VersionInfo(0, 1, 0, mobase.ReleaseType.prealpha)

    def isActive(self):
        """
        @brief called to test if this plugin is active. inactive plugins can still be configured
            and report problems but otherwise have no effect.
            For game plugins this is currently ignored during instance creation!
        @return true if this plugin is active.
        """
        return True

    def settings(self):
        """
        @return list of configurable settings for this plugin. The list may be empty.
        This could be used for example to allow users to change some of the parameters of this plugin.
        Example: [mobase.PluginSetting("enabled", self.__tr("Enable this plugin), True)]
        To retrieve it: isEnabled = self.__organizer.pluginSetting(self.name(), "enabled")
        """
        return []    

    """
    Here IPluginGame interface stuff. 
    """

    def gameName(self):
        """
        @return name of the game.
        """
        return "Darkest Dungeon"
    
    def gameShortName(self):
        """
        @brief Get the 'short' name of the game.
        
        The short name of the game is used for savegames, registry entries,
        Nexus API calls and some MO2 internal settings storage.
        """
        return "darkestdungeon"
    
    def gameIcon(self):
        """
        @return an icon for this game (QIcon constructor accepts a path).
        """
        return QIcon()

    def validShortNames(self):
        """
        @brief Get the list of valid game names, this is also used to accept alternative game sources.
            Eg: Skyrim nexus for SSE.
        
        Originally the short name was used for Nexus stuff but then Nexus changed the game identifiers
        forcing Mo2 to add the gameNexusName() to use the correct one.
        """
        return [self.gameShortName()]

    def gameNexusName(self):
        """
        @brief get the Nexus name of the game, used for API calls and for mod pages resolution.
        """
        return "darkestdungeon"
    
    def nexusModOrganizerID(self):
        """
        @brief Get the Nexus ID of the Mod Organizer page for this game.
        Use 0 if no page exists.
        """
        return 0
    
    def nexusGameID(self):
        """
        @brief Get the Nexus Game ID.
        """
        return 804
    
    def steamAPPId(self):
        """
        @return steam app id for this game. Should be empty for games not available on steam
        @note if a game is available in multiple versions those might have different app ids.
            the plugin should try to return the right one
        """
        return "262060"
    
    def binaryName(self):
        """
        @brief Get the name of the executable that gets run
        """
        return "_windows/Darkest.exe"
    
    def getLauncherName(self):
        """
        @brief Get the name of the game launcher
        """
        return ""

    def executables(self):
        """
        @return list of automatically discovered executables of the game itself and tools surrounding it.
        """
        game = mobase.ExecutableInfo("Darkest Dungeon", QFileInfo(self.m_GameDir, "_windows/Darkest.exe"))
        game.withWorkingDirectory(self.m_GameDir)
        return [game]

    def savegameExtension(self):
        """
        @return file extension of save games for this game.
        """
        return ""
    
    def savegameSEExtension(self):
        """
        @return file extension of script extender save game files for this game.
        """
        return ""

    def initializeProfile(self, path, settings):
        """
        @brief initialize a profile for this game.
        @param path the directory where the profile is to be initialized.
        @param settings parameters for how the profile should be initialized.
        @note this function will be used to initially create a profile, potentially to repair it or upgrade/downgrade it so the implementations
            have to gracefully handle the case that the directory already contains files!
        """
        pass
    
    def primaryPlugins(self):
        """
        @return list of plugins that are part of the game and not considered optional.
        """
        return []
    
    def gameVariants(self):
        """
        @return list of game variants
        @note If there are multiple variants of a game (and the variants make a difference to the
            plugin) like a regular one and a GOTY-edition the plugin can return a list of them and
            the user gets to chose which one he owns.
        """
        return []
    
    def setGameVariant(self, variantStr):
        """
        @brief if there are multiple game variants (returned by gameVariants) this will get called
            on start with the user-selected game edition allowing for manual internal adjustments.
        @param variant the game edition selected by the user
        """
        pass

    def gameVersion(self):
        """
        @brief return version of the managed game.
        """
        return "1"
    
    def iniFiles(self):
        """
        @brief Get the list of .ini files this game uses.

        @note just the name, these are all assumed residing in the documentsDirectory().
        @note It is important that the 'main' .ini file comes first in this list.
        """
        return []
    
    def DLCPlugins(self):
        """
        @brief Get a list of esp/esm files that are part of known dlcs.
        """
        return []
    
    def CCPlugins(self):
        """
        @brief Get the current list of active Creation Club plugins.
        """
        return []
    
    def loadOrderMechanism(self):
        """
        @brief determine the load order mechanism used by this game.

        @note this may throw an exception if the mechanism can't be determined.

        Either:
            FileTime,
            PluginsTxt
        
        Leave to PluginsTxt in case the game does not use plugins.
        """
        return mobase.LoadOrderMechanism.PluginsTxt
    
    def sortMechanism(self):
        """
        @brief determine the sorting mech
        Either:
            NONE,
            MLOX,
            BOSS,
            LOOT
        """
        return mobase.SortMechanism.NONE
    
    def looksValid(self, aQDir):
        """
        @brief See if the supplied directory looks like a valid installation of the game.
        """
        return QFileInfo(aQDir.path() + "/_windows/Darkest.exe").exists()
    
    def isInstalled(self):
        """
        @return true if this game has been discovered as installed, false otherwise.
        
        Used to allow fast instance creation. This function can be used to check
        registry keys for the path of the game and setting the internal game/data directories.
        """

        """
        HKEY_CURRENT_USER\\Software\\Valve\\Steam\\Apps\\262060 contains Installed
        HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Steam App 262060 has InstallLocation
        https://github.com/ModOrganizer2/modorganizer-game_gamebryo/blob/master/src/gamebryo/gamegamebryo.cpp#L299
        """
        return False
    
    def gameDirectory(self):
        """
        @return directory to the game installation.
        """
        return self.m_GameDir
    
    def dataDirectory(self):
        """
        @return directory where the game expects to find its data files (virtualization target).
        """
        return self.m_DataDir
    
    def setGamePath(self, pathStr):
        """
        @brief set the path to the managed game.
        @param path to the game.
        @note this will be called by by MO to set the concrete path of the game. This is particularly
            relevant if the path wasn't auto-detected but had to be set manually by the user.
        """
        self.m_GameDir=QDir(pathStr)
        self.m_DataDir=QDir(self.m_GameDir.path() + "/mods/")
    
    def documentsDirectory(self):
        """
        @return directory of the documents folder where configuration files and such for this game reside.
        """
        return QDir("{}/My Games".format(os.getenv("CSIDL_MYDOCUMENTS")))
    
    def savesDirectory(self):
        """
        @return path to where save games are stored.
        """
        return self.documentsDirectory()
    
    def _featureList(self):
        """
        Map of features that the game supports where each feature is a class abiding to
        an interface of one of the supported features found in the game_features project
        on the Modorganizer2 github.

        GamePlugins feature is currently mandatory as Mo2 will otherwise crash.
        """
        return self.__featureMap
    
    def __tr(self, str):
        return QCoreApplication.translate("DarkestDungeon", str)
    
def createPlugin():
    return DarkestDungeon()
