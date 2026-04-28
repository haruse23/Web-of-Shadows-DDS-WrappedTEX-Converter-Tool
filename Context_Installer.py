import winreg as reg
import os
import sys
from pathlib import Path


SCRIPT_NAME = "Convert.py"


ALL_PATHS = ["Software\\Classes\\SystemFileAssociations\\.dds\\shell\\DDStoWrappedTEX (WoS)", "Software\\Classes\\SystemFileAssociations\\.tex\\shell\\WrappedTEXtoDDS (WoS)"]


IS_PATH_END = ["SOFTWARE", "CLASSES", "SYSTEMFILEASSOCIATIONS"] # Can't end in Software, Classes, SystemFileAssociations

            
HIVES = [reg.HKEY_CURRENT_USER,
         reg.HKEY_LOCAL_MACHINE,
         reg.HKEY_CLASSES_ROOT]
         
         
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

def print_key(root, path, indent=0):
    try:
        with reg.OpenKey(root, path, 0, reg.KEY_READ) as key:

            print("  " * indent + f"[KEY] {path}")

    except FileNotFoundError:
        print("  " * indent + f"[MISSING] {path}")
        return False
        
    except PermissionError:
        print("  " * indent + f"[DENIED] {path}")
        return False
        
        
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
        
        
        print(f"Follwing paths will be registered for .dds and .wrap.tex in HKEY_CURRENT_USER: {key_path}")
        print(f"Follwing paths will be registered for .dds and .wrap.tex in HKEY_CURRENT_USER: {key_path + "\\command"}")
        install_context_menu = input("Do you want to install context menus ?\n")
        
        if install_context_menu == "yes":
            with reg.CreateKey(reg.HKEY_CURRENT_USER, key_path) as key:
                reg.SetValue(key, "", reg.REG_SZ, menu_text)
                reg.SetValueEx(key, "Position", 0, reg.REG_SZ, "Bottom")   # Try to put at bottom
        
            # Build the command
            python_path = get_python_path()
            script_full_path = get_script_full_path()
            
            command_line = f'"{python_path}" "{script_full_path}" "%1"'

            command_path = rf"{key_path}\command"
            with reg.CreateKey(reg.HKEY_CURRENT_USER, command_path) as cmd_key:
                reg.SetValue(cmd_key, "", reg.REG_SZ, command_line)

            print(f"✓ Successfully added for {extension}")
            
        else:
            print("Nothing has been executed. Nothing has been registered.")
        
    except Exception as e:
        print(f"✗ Failed for {extension}: {e}")



def delete_key(root, path):
    try:
        # Open the key
        with reg.OpenKey(root, path, 0, reg.KEY_ALL_ACCESS) as key:
            
            # Delete subkeys first
            while True:
                try:
                    subkey = reg.EnumKey(key, 0)
                    delete_key(root, path + "\\" + subkey)
                except OSError:
                    break
                    
            # Delete values
            while True:
                try:
                    value = reg.EnumValue(key, 0)[0]
                    reg.DeleteValue(key, value)
                except OSError:
                    break
                    
        # Now delete the key itself
        reg.DeleteKey(root, path)
        print(f"✓ Deleted {path}")
        
    except FileNotFoundError:
        print(f"Key not found: {path}")
    except PermissionError:
        print("✗ Permission denied (run as admin)")
    except Exception as e:
        print("✗ Error:", e)
        
        
def remove_context_menu():
    try:
        for hive in HIVES:
            for path in ALL_PATHS:
                print_key_info = print_key(hive, path)
                
                if print_key_info == False:
                    continue
                
                uninstall = input("Are you sure you want to delete/unregister this path (key) ?\n")
                
                if uninstall == "yes":
                    if path == "" or path.split("\\")[-1].upper() in IS_PATH_END: # Safe-guard. Check if path is empty or its uppercase format ends in any of the string elements inside IS_PATH_END List
                        print("You can't unregister/delete this !!. Aborting...")
                        return
                        
                        
                    delete_key(hive, path)
                    
                    print("✓ Successfully removed key from registry")
                    
                else:
                    print("Key/path hasn't been removed from registry")

        return


    except PermissionError:
        print("✗ Permission denied (run as admin)")
        return
    except Exception as e:
        print("✗ Error:", e)
        return



def main():
    print("=== DDS / Wrapped TEX Converter - Context Menu Installer ===\n")
    
    script_full = get_script_full_path()
    print(f"Using script: {script_full}\n")
    
    register = input("Do you want to install this ?\n")
    
    if register == "yes":
        for ext, info in MENU_ITEMS.items():
            add_context_menu(ext, info["text"], info["key_name"])
    
    elif register == "no":
            remove_context_menu()

    print("\nCode finished!")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()