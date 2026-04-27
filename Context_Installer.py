import winreg as reg
import os
import sys
from pathlib import Path


SCRIPT_NAME = "Convert.py"

# Different text for each extension
MENU_ITEMS = {
    ".dds": {
        "text": "Convert to .wrap.tex (WoS)",         # What user sees on .dds files
        "key_name": "DDStoWrappedTEX (WoS)"
    },
    ".tex": {
        "text": "Convert to .dds (WoS)",         # What user sees on .tex files
        "key_name": "WrappedTEXtoDDS (WoS)"
    }
}

EXTENSIONS = [".dds", ".tex"]
# ===================================================

def get_python_path():
    python_exe = Path(sys.executable)
    python = python_exe.parent / "pythonw.exe"
    
    if python.exists():
        return str(python)

def get_script_full_path():

    # If the installer and script are in the same folder
    script_path = Path(__file__).parent / SCRIPT_NAME
    
    if script_path.exists():
        return str(script_path.resolve())
    else:
        # Ask user to enter full path manually if not found
        print(f"Could not find {SCRIPT_NAME} in the current folder.")
        manual_path = input("Please enter the FULL path to your converter script: ").strip().strip('"')
        return manual_path

def add_context_menu(extension, menu_text, menu_key):
    base_key = rf"Software\Classes\SystemFileAssociations\{extension}\shell"

    try:
        key_path = rf"{base_key}\{menu_key}"
        
        with reg.CreateKey(reg.HKEY_LOCAL_MACHINE, key_path) as key:
            reg.SetValue(key, "", reg.REG_SZ, menu_text)
            reg.SetValueEx(key, "Position", 0, reg.REG_SZ, "Bottom")   # Try to put at bottom

        # Build the command
        python_path = get_python_path()
        script_full_path = get_script_full_path()
        
        command_line = f'"{python_path}" "{script_full_path}" "%1"'

        command_path = rf"{key_path}\command"
        with reg.CreateKey(reg.HKEY_LOCAL_MACHINE, command_path) as cmd_key:
            reg.SetValue(cmd_key, "", reg.REG_SZ, command_line)

        print(f"✓ Successfully added for {extension}")
        
    except Exception as e:
        print(f"✗ Failed for {extension}: {e}")


def remove_context_menu(extension, menu_key):
    """Unregister a context menu item for a file extension"""
    base_key = rf"Software\Classes\SystemFileAssociations\{extension}\shell"
        
    key_path = rf"{base_key}\{menu_key}"
    
    try:
        # First, delete the command subkey
        command_path = rf"{key_path}\command"
        try:
            reg.DeleteKey(reg.HKEY_LOCAL_MACHINE, command_path)
            print(f"  ✓ Deleted command key")
        except FileNotFoundError:
            pass  # Key doesn't exist, that's fine
        
        # Then delete the menu key itself
        reg.DeleteKey(reg.HKEY_LOCAL_MACHINE, key_path)
        print(f"✓ Successfully unregistered '{menu_key}' for {extension}")
        return True
        
    except PermissionError:
        print(f"✗ Permission denied for {extension}. Run as Administrator!")
        return False
    except FileNotFoundError:
        print(f"✗ Context menu not found for {extension}\\{menu_key}")
        return False
    except Exception as e:
        print(f"✗ Failed to unregister for {extension}: {e}")
        return False



def main():
    print("=== DDS / Wrapped TEX Converter - Context Menu Installer ===\n")
    
    script_full = get_script_full_path()
    print(f"Using script: {script_full}\n")
    
    register = input("Do you want to install this ?")
    
    if register == "yes":
        for ext, info in MENU_ITEMS.items():
            add_context_menu(ext, info["text"], info["key_name"])
    
    elif register == "no":
        for ext, info in MENU_ITEMS.items():
            remove_context_menu(ext, info["key_name"])

    print("\nCode finished!")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()