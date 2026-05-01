# Web-of-Shadows-DDS-WrappedTEX-Converter-Tool
This tool is designed as a better alternative to the .dds/.wrap.tex conversion functionality in my [WoS BlenderToolkit](https://github.com/haruse23/WoS-BlenderToolkit).

Instead of having to run Blender to convert to .dds or .wrap.tex, you just right-click one of those files and you see an option in the menu to convert.

This will be very useful for mod creators who work with game files too much.

The tool can be installed or un-installed.

For more details, read the "How To Install.txt" file, it also includes how to un-install.

# Changelog
### Version 1.0.3
- Changed the tool such that it uses pythonw.exe instead, which shows no console windows. However, this way if any errors occur we won't be able to catch them, unless the Convert.py script is ran normally from the CMD

- Changed the tool such that it un-registers the keys from only the current user's hive where they were added (HKEY_CURRENT_USER)

- Changed the tool such that it sets the default value as "open", now when double-clicking the default Windows's Open/Open With... will execute instead of the tool itself

- Changed the tool such that it bypasses WIndows's 15 file limit through the value "MultiSelectModel"="Player", now more than 15 files can be selected and the tool will still show in the Context Menu

### Version 1.0.2
- Made the tool so it is much safer, now it asks for more confirmation before registering or unregistering any path or key

### Version 1.0.1
- Changed the tool to register only to the current user's hive (HKEY_CURRENT_USER), read the "How To Install.txt" file very well.
- Changed the tool to un-register from all three hives [HKEY_CLASSES_ROOT, HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE] just in case anything gets duplicated

### Version 1.0.0
- Release

