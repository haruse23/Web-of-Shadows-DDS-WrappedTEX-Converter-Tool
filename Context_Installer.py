import winreg as reg
import os
import sys
from pathlib import Path


SCRIPT_NAME = "Convert.py"


ALL_PATHS = ["Software\\Classes\\WoSTextureTool", "Software\\Classes\\SystemFileAssociations\\.tex", "Software\\Classes\\SystemFileAssociations\\.dds\\shell\\WoSTextureTool (Convert to .wrap.tex)"]


IS_PATH_END = ["SOFTWARE", "CLASSES", "SYSTEMFILEASSOCIATIONS"] # Can't end in Software, Classes, SystemFileAssociations

            
HIVES = [reg.HKEY_CURRENT_USER,
         reg.HKEY_LOCAL_MACHINE, # No need to use, ignore
         reg.HKEY_CLASSES_ROOT] # No need to use, ignore
         
         
# Different text for each extension
MENU_ITEMS = {
    ".dds": {
        "text": "WebOfShadows (Convert to .wrap.tex)",         # What user sees on .dds files
    },
    ".tex": {
        "text": "WebOfShadows (Convert to .dds)",         # What user sees on .tex files
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


"""def add_WoSTextureTool_FileHandler(tex_item):
    try:
        base_key = rf"Software\\Classes\\WoSTextureTool"
        
        print(f"Follwing paths will be registered for WoSTextureTool Filehandler in HKEY_CURRENT_USER: {base_key}")
        print(f"Follwing paths will be registered for WoSTextureTool Filehandler in HKEY_CURRENT_USER: {base_key}\\\\shell")
        print(f"Follwing paths will be registered for WoSTextureTool Filehandler in HKEY_CURRENT_USER: {base_key}\\\\shell\\\\{tex_item["text"]}")
        print(f"Follwing paths will be registered for WoSTextureTool Filehandler in HKEY_CURRENT_USER: {base_key}\\\\shell\\\\{tex_item["text"]}\\\\command")
            
        install_filehandler = input("Do you want to install WoSTextureTool Filehandler ? (yes/no)\n")
        print()
        
        if install_filehandler == "yes":
            with reg.CreateKey(reg.HKEY_CURRENT_USER, f"{base_key}\\shell\\{tex_item["text"]}") as key:
                reg.SetValueEx(key, "Position", 0, reg.REG_SZ, "Bottom")
            
            
            with reg.CreateKey(reg.HKEY_CURRENT_USER, f"{base_key}\\shell\\{tex_item["text"]}\\command") as key:
            
                # Build the command
                python_path = get_python_path()
                script_full_path = get_script_full_path()
                
                command_line = f'cmd.exe /k ""{python_path}" "{script_full_path}" "%1""'
                

                reg.SetValueEx(key, "", 0, reg.REG_SZ, command_line)

                print(f"✓ Successfully added for WoSTextureTool Filehandler")
                print()
        
        else:
            print("Nothing has been executed. Nothing has been registered.")
            print()

    
    except Exception as e:
        print(f"✗ Failed for WoSTextureTool Filehandler: {e}")"""
        





    
def add_context_menu(extension, menu_text):
    base_key_dds = rf"Software\\Classes\\SystemFileAssociations\\{extension}"
    
    base_key_tex = rf"Software\\Classes\\{extension}"
    base_key_tex_SFA = rf"Software\\Classes\\SystemFileAssociations\\{extension}"
    

    try:
        if extension == ".dds":
            print(f"All the follwing keys will be registered for {extension} in HKEY_CURRENT_USER: {base_key_dds}\\shell\\{menu_text}\\command")
            
        if extension == ".tex":
            print(f"All the follwing keys will be registered for {extension} in HKEY_CURRENT_USER: {base_key_tex}\\shell")
            print(f"All the follwing keys will be registered for {extension} in HKEY_CURRENT_USER: {base_key_tex_SFA}\\shell\\WebOfShadows\\command")
            
        install_context_menu = input("Do you want to install context menus ? (yes/no)\n")
        print()
        
        if install_context_menu == "yes":
            if extension == ".dds":
                with reg.CreateKey(reg.HKEY_CURRENT_USER, f"{base_key_dds}\\shell\\") as key:
                    reg.SetValueEx(key, "", 0, reg.REG_SZ, "open") # Set default action when double-clicking to Open if there is a default associated app, otherwise Open with...
            
                with reg.CreateKey(reg.HKEY_CURRENT_USER, f"{base_key_dds}\\shell\\{menu_text}") as key:
                    reg.SetValueEx(key, "Position", 0, reg.REG_SZ, "Bottom")   # Place at the bottom
            
                # Build the command
                python_path = get_python_path()
                script_full_path = get_script_full_path()
                
                command_line = f'"{python_path}" "{script_full_path}" "%1"'

                command_path = rf"{base_key_dds}\\shell\\{menu_text}\\command"
                
                with reg.CreateKey(reg.HKEY_CURRENT_USER, command_path) as cmd_key:
                    reg.SetValueEx(cmd_key, "", 0, reg.REG_SZ, command_line)

                print(f"✓ Successfully added for {extension}")
                print()
            
            
            if extension == ".tex":
                reg.CreateKey(reg.HKEY_CURRENT_USER, f"{base_key_tex}\\shell")
                
                with reg.CreateKey(reg.HKEY_CURRENT_USER, f"{base_key_tex_SFA}\\shell\\") as key:
                    reg.SetValueEx(key, "", 0, reg.REG_SZ, "open") # Set default action when double-clicking to Open if there is a default associated app, otherwise Open with...
            
                with reg.CreateKey(reg.HKEY_CURRENT_USER, f"{base_key_tex_SFA}\\shell\\{menu_text}") as key:
                    reg.SetValueEx(key, "Position", 0, reg.REG_SZ, "Bottom") # Place at the bottom
                    reg.SetValueEx(key, "MultiSelectModel", 0, reg.REG_SZ, "Player") # Bypass windows 15 file limit
                
                # Build the command
                python_path = get_python_path()
                script_full_path = get_script_full_path()
                
                command_line = f'"{python_path}" "{script_full_path}" "%1"'

                with reg.CreateKey(reg.HKEY_CURRENT_USER, f"{base_key_tex_SFA}\\shell\\{menu_text}\\command") as key:
                    reg.SetValueEx(key, "", 0, reg.REG_SZ, command_line)
                    
                print(f"✓ Successfully added for {extension}")
                print()
            
            
        else:
            print("Nothing has been executed. Nothing has been registered.")
            print()
        
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
        for path in ALL_PATHS:
            print_key_info = print_key(hive, path)
            
            if print_key_info == False:
                continue
            
            uninstall = input("Are you sure you want to delete/unregister this path (key) ? (yes/no)\n")
            
            if uninstall == "yes":
                if path == "" or path.split("\\")[-1].upper() in IS_PATH_END: # Safe-guard. Check if path is empty or its uppercase format ends in any of the string elements inside IS_PATH_END List
                    print("You can't unregister/delete this !!. Aborting...")
                    return
                    
                    
                delete_key(reg.HKEY_CURRENT_USER, path)
                
                print("✓ Successfully removed key from registry")
                print()
                
            else:
                print("Key/path hasn't been removed from registry")
                print()

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
    
    register = input("Do you want to install this ? (yes/no)\n")
    print()
    
    if register == "yes":
        for ext, info in MENU_ITEMS.items():
            add_context_menu(ext, info["text"])
    
    elif register == "no":
            remove_context_menu()

    print("\nCode finished!")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()