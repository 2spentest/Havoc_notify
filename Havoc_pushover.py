import os
import requests
import havocui
from havoc import Demon, Event

# Global variables for Pushover keys and selected items
pushover_user_key = ""
pushover_api_token = ""
pushover_user_key = ""
pushover_api_token = ""
send_username = True
send_listener = True
send_external_ip = True
send_internal_ip = True
send_hostname = True
send_domain = True
send_os = True
send_os_build = True
send_os_arch = True
send_process_name = True
send_process_id = True
send_process_arch = True

save_keys = False
keys_file = os.path.join(os.path.expanduser("~"), ".config", ".pushover")


def load_keys():
    """Load Pushover keys from file if it exists."""
    global pushover_user_key, pushover_api_token
    if os.path.exists(keys_file):
        with open(keys_file, "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                pushover_user_key = lines[0].strip()
                pushover_api_token = lines[1].strip()

def save_keys_to_file():
    """Save Pushover keys to file."""
    if save_keys:
        with open(keys_file, "w") as f:
            f.write(f"{pushover_user_key}\n{pushover_api_token}\n")

def send_pushover_notification(message):
    """Send a Pushover notification."""
    try:
        payload = {
            'token': pushover_api_token,
            'user': pushover_user_key,
            'message': message
        }
        response = requests.post('https://api.pushover.net/1/messages.json', data=payload)
    except Exception as e:
        print(f"Exception occurred while sending Pushover notification: {e}")

def alert_new_demon(demonID):
    """Callback function for new daemon connections."""
    try:
        demon = Demon(demonID)
        message = "New demon connected"
        if send_listener:
            listener = getattr(demon, 'Listener', 'Unknown Listener')  # Providing a default if 'Listener' is None
            message += f"\nListener: {listener}"
        if send_external_ip:
            message += f"\nExternal IP: {demon.ExternalIP}"
        if send_internal_ip:
            message += f"\nInternal IP: {demon.InternalIP}"
        if send_username:
            message += f"\nUsername: {demon.User}"
        if send_hostname:
            message += f"\nHostname: {demon.Computer}"
        if send_domain:
            message += f"\nDomain: {demon.Domain}"
        if send_os:
            message += f"\nOS: {demon.OS}"
        if send_os_build:
            message += f"\nOS Build: {demon.OSBuild}"
        if send_os_arch:
            message += f"\nOS Architecture: {demon.OSArch}"
        if send_process_name:
            message += f"\nProcess Name: {demon.ProcessName}"
        if send_process_id:
            message += f"\nProcess ID: {demon.ProcessID}"
        if send_process_arch:
            message += f"\nProcess Architecture: {demon.ProcessArch}"
        send_pushover_notification(message)
    except Exception as e:
        print(f"Exception occurred in alert_new_demon: {e}")

def open_pushover_gui():
    """Open the GUI for Pushover configuration."""
    try:
        global pushover_user_key, pushover_api_token
        pushover_gui.clear()
        pushover_gui.addLabel("<h2 style='color:#bd93f9'>Pushover Configuration</h2>")
        pushover_gui.addLabel("<span style='color:#71e0cb'>Pushover User Key:</span>")
        pushover_gui.addLineedit(pushover_user_key, set_user_key)
        pushover_gui.addLabel("<span style='color:#71e0cb'>Pushover API Token:</span>")
        pushover_gui.addLineedit(pushover_api_token, set_api_token)
        pushover_gui.addLabel("<h3 style='color:#bd93f9'>Options</h3>")
        pushover_gui.addCheckbox("Save keys to file", toggle_save_keys, save_keys)
        pushover_gui.addCheckbox("Send Listener", toggle_send_listener, send_listener)
        pushover_gui.addCheckbox("Send External IP", toggle_send_external_ip, send_external_ip)
        pushover_gui.addCheckbox("Send Internal IP", toggle_send_internal_ip, send_internal_ip)
        pushover_gui.addCheckbox("Send Username", toggle_send_username, send_username)
        pushover_gui.addCheckbox("Send Hostname", toggle_send_hostname, send_hostname)
        pushover_gui.addCheckbox("Send Domain", toggle_send_domain, send_domain)
        pushover_gui.addCheckbox("Send OS", toggle_send_os, send_os)
        pushover_gui.addCheckbox("Send OS Build", toggle_send_os_build, send_os_build)
        pushover_gui.addCheckbox("Send OS Architecture", toggle_send_os_arch, send_os_arch)
        pushover_gui.addCheckbox("Send Process Name", toggle_send_process_name, send_process_name)
        pushover_gui.addCheckbox("Send Process ID", toggle_send_process_id, send_process_id)
        pushover_gui.addCheckbox("Send Process Architecture", toggle_send_process_arch, send_process_arch)
        pushover_gui.addButton("Save and Start", save_keys_and_start)
        pushover_gui.setSmallTab()
    except Exception as e:
        print(f"Exception occurred in open_pushover_gui: {e}")



def toggle_save_keys():
    """Toggle the save keys checkbox state."""
    global save_keys
    try:
        save_keys = not save_keys
    except Exception as e:
        print(f"Exception occurred in toggle_save_keys: {e}")

def toggle_send_listener():
    """Toggle the send listener checkbox state."""
    global send_listener
    try:
        send_listener = not send_listener
    except Exception as e:
        print(f"Exception occurred in toggle_send_listener: {e}")

def toggle_send_external_ip():
    """Toggle the send external IP checkbox state."""
    global send_external_ip
    try:
        send_external_ip = not send_external_ip
    except Exception as e:
        print(f"Exception occurred in toggle_send_external_ip: {e}")

def toggle_send_internal_ip():
    """Toggle the send internal IP checkbox state."""
    global send_internal_ip
    try:
        send_internal_ip = not send_internal_ip
    except Exception as e:
        print(f"Exception occurred in toggle_send_internal_ip: {e}")

def toggle_send_username():
    """Toggle the send username checkbox state."""
    global send_username
    try:
        send_username = not send_username
    except Exception as e:
        print(f"Exception occurred in toggle_send_username: {e}")

def toggle_send_hostname():
    """Toggle the send hostname checkbox state."""
    global send_hostname
    try:
        send_hostname = not send_hostname
    except Exception as e:
        print(f"Exception occurred in toggle_send_hostname: {e}")

def toggle_send_domain():
    """Toggle the send domain checkbox state."""
    global send_domain
    try:
        send_domain = not send_domain
    except Exception as e:
        print(f"Exception occurred in toggle_send_domain: {e}")

def toggle_send_os():
    """Toggle the send OS checkbox state."""
    global send_os
    try:
        send_os = not send_os
    except Exception as e:
        print(f"Exception occurred in toggle_send_os: {e}")

def toggle_send_os_build():
    """Toggle the send OS build checkbox state."""
    global send_os_build
    try:
        send_os_build = not send_os_build
    except Exception as e:
        print(f"Exception occurred in toggle_send_os_build: {e}")

def toggle_send_os_arch():
    """Toggle the send OS architecture checkbox state."""
    global send_os_arch
    try:
        send_os_arch = not send_os_arch
    except Exception as e:
        print(f"Exception occurred in toggle_send_os_arch: {e}")

def toggle_send_process_name():
    """Toggle the send process name checkbox state."""
    global send_process_name
    try:
        send_process_name = not send_process_name
    except Exception as e:
        print(f"Exception occurred in toggle_send_process_name: {e}")

def toggle_send_process_id():
    """Toggle the send process ID checkbox state."""
    global send_process_id
    try:
        send_process_id = not send_process_id
    except Exception as e:
        print(f"Exception occurred in toggle_send_process_id: {e}")

def toggle_send_process_arch():
    """Toggle the send process architecture checkbox state."""
    global send_process_arch
    try:
        send_process_arch = not send_process_arch
    except Exception as e:
        print(f"Exception occurred in toggle_send_process_arch: {e}")

def set_user_key(text):
    """Set the Pushover User Key."""
    global pushover_user_key
    try:
        print(f"Setting Pushover User Key: {text}")
        pushover_user_key = text
    except Exception as e:
        print(f"Exception occurred in set_user_key: {e}")

def set_api_token(text):
    """Set the Pushover API Token."""
    global pushover_api_token
    try:
        print(f"Setting Pushover API Token: {text}")
        pushover_api_token = text
    except Exception as e:
        print(f"Exception occurred in set_api_token: {e}")

def save_keys_and_start():
    """Save the Pushover keys and start monitoring."""
    try:
        if not pushover_user_key or not pushover_api_token:
            print("Pushover User Key and API Token are required")
            havocui.errormessage("Please enter both the Pushover User Key and API Token.")
        else:
            print(f"Saving keys and starting event monitoring. Save keys: {save_keys}")
            save_keys_to_file()
            event = Event("events")
            event.OnNewSession(alert_new_demon)
            print("Pushover keys saved and script started.")
    except Exception as e:
        print(f"Exception occurred in save_keys_and_start: {e}")

# Load keys from file if they exist
load_keys()

# Create Pushover GUI tab
try:
    pushover_gui = havocui.Widget("Pushover Configuration", True)
    havocui.createtab("Pushover Config", "Pushover", open_pushover_gui)
except Exception as e:
    print(f"Exception occurred while creating GUI tab: {e}")

