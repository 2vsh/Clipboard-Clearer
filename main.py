import os
import keyboard
import subprocess
import threading
import time

CONFIG_FILE = 'keybind_config.txt'

def clear_clipboard():
    subprocess.run("echo off | clip", shell=True)
    print("Clipboard cleared.")

def listen_for_key_combination(key_combination):
    keyboard.add_hotkey(key_combination, clear_clipboard)
    # Keep the script running and listening for the hotkey
    keyboard.wait()

def get_key_combination():
    print("Press the key combination you want to use for the keybind. When 5 seconds have passed without a new key being pressed, it will be locked in as the keybind.")

    key_combination = []
    last_key_time = time.time()

    def on_key_event(event):
        nonlocal last_key_time
        if event.event_type == keyboard.KEY_DOWN and event.name not in key_combination:
            key_combination.append(event.name)
            print(f"Key pressed: {event.name}")
        last_key_time = time.time()
 
    keyboard.hook(on_key_event)

    while time.time() - last_key_time < 5:
        time.sleep(0.1)
    
    keyboard.unhook_all()
    key_combination_str = '+'.join(key_combination)
    print(f"Key combination '{key_combination_str}' registered as keybind.")
    return key_combination_str

def read_keybind_from_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            key_combination = file.read().strip()
            if key_combination:
                return key_combination
    return None

def write_keybind_to_config(key_combination):
    with open(CONFIG_FILE, 'w') as file:
        file.write(key_combination)

# Check for existing keybind in the config file
key_combination = read_keybind_from_config()

if not key_combination:
    # If no keybind is found or the config file is cleared, get a new keybind from the user
    key_combination = get_key_combination()
    write_keybind_to_config(key_combination)

# Run the listener in a separate thread to keep it headless
listener_thread = threading.Thread(target=listen_for_key_combination, args=(key_combination,), daemon=True)
listener_thread.start()

# Keep the main thread running to allow the listener to work in the background
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Script stopped.")
