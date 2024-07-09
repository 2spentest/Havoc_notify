import os
import requests
import havocui
from havoc import Demon, Event

# Global variables for Pushover keys and selected items
pushover_config = {
    'user_key': '',
    'api_token': ''
}

teams_config = {
    'webhook_url': ''
}

notified_demons = set()

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

save_keys = True
config_dir = os.path.join(os.path.expanduser("~"), ".config", "notification_service")
notified_demons_file = os.path.join(config_dir, "notified_demons.txt")
options_file = os.path.join(config_dir, "options_config.txt")


# Function to load configuration from file
def load_config(service):
    config_path = os.path.join(config_dir, f"{service}_config.txt")
    print(f"Loading config for {service} from {config_path}")
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) < 2:
                    print(f"Skipping malformed line: {line}")
                    continue
                key, value = parts[0], ":".join(parts[1:])  # Rejoin in case value contains colons
                if service == 'pushover':
                    pushover_config[key] = value
                elif service == 'teams':
                    teams_config[key] = value
    print(f"Loaded config for {service}: {pushover_config if service == 'pushover' else teams_config}")



# Function to save configuration to file
def save_config(service):
    config_path = os.path.join(config_dir, f"{service}_config.txt")
    print(f"Saving config for {service} to {config_path}")
    with open(config_path, "w") as file:
        if service == 'pushover':
            for key, value in pushover_config.items():
                file.write(f"{key}:{value}\n")
        elif service == 'teams':
            for key, value in teams_config.items():
                file.write(f"{key}:{value}\n")
    print(f"Saved config for {service}")

# Function to load options from file
def load_options():
    print(f"Loading options from {options_file}")
    if os.path.exists(options_file):
        with open(options_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split(":")
                globals()[key] = value == 'True'
    print(f"Loaded options: {globals()}")

# Function to save options to file
def save_options():
    print(f"Saving options to {options_file}")
    with open(options_file, "w") as file:
        options = [
            'save_keys', 'send_listener', 'send_external_ip', 'send_internal_ip',
            'send_username', 'send_hostname', 'send_domain', 'send_os', 'send_os_build',
            'send_os_arch', 'send_process_name', 'send_process_id', 'send_process_arch'
        ]
        for option in options:
            file.write(f"{option}:{globals()[option]}\n")
    print(f"Saved options")



def load_notified_demons():
    if os.path.exists(notified_demons_file):
        with open(notified_demons_file, "r") as file:
            for line in file:
                notified_demons.add(line.strip())

def save_notified_demon(demonID):
    os.makedirs(config_dir, exist_ok=True)

    # Ensure the file exists before appending
    if not os.path.exists(notified_demons_file):
        with open(notified_demons_file, "w") as file:
            pass  # Create the file if it doesn't exist

    with open(notified_demons_file, "a") as file:
        file.write(f"{demonID}\n")

# Function to send Pushover notification
def send_pushover_notification(message):
    if not pushover_config['user_key'] or not pushover_config['api_token']:
        print("Pushover keys not set, skipping notification")
        return
    payload = {
        'token': pushover_config['api_token'],
        'user': pushover_config['user_key'],
        'message': message
    }
    response = requests.post('https://api.pushover.net/1/messages.json', data=payload)
    print(f"Pushover response: {response.status_code}, {response.text}")

# Function to send Teams notification
def send_teams_notification(message):
    if not teams_config['webhook_url']:
        print("Teams webhook URL not set, skipping notification")
        return

    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": message,
                            "wrap": True
                        }
                    ],
                    "version": "1.0"
                }
            }
        ]
    }

    response = requests.post(teams_config['webhook_url'], json=payload)
    print(f"Teams response: {response.status_code}, {response.text}")

# Callback function for new daemon connections
def alert_new_demon(demonID):
    if demonID in notified_demons:
        print(f"Daemon {demonID} already notified.")
        return
    try:
        demon = Demon(demonID)
        message = (
           "New demon connected\n"
           f"Listener: {demon.Listener if demon.Listener else 'None'}\n"
           f"External IP: {demon.ExternalIP if demon.ExternalIP else 'None'}\n"
           f"Internal IP: {demon.InternalIP if demon.InternalIP else 'None'}\n"
           f"Username: {demon.User if demon.User else 'None'}\n"
           f"Hostname: {demon.Computer if demon.Computer else 'None'}\n"
           f"Domain: {demon.Domain if demon.Domain else 'None'}\n"
           f"OS: {demon.OS if demon.OS else 'None'}\n"
           f"OS Build: {demon.OSBuild if demon.OSBuild else 'None'}\n"
           f"OS Architecture: {demon.OSArch if demon.OSArch else 'None'}\n"
           f"Process Name: {demon.ProcessName if demon.ProcessName else 'None'}\n"
           f"Process ID: {demon.ProcessID if demon.ProcessID else 'None'}\n"
           f"Process Architecture: {demon.ProcessArch if demon.ProcessArch else 'None'}"
        )

        print(f"Sending notification for new demon: {message}")
        send_pushover_notification(message)
        send_teams_notification(message)

        notified_demons.add(demonID)
        save_notified_demon(demonID)
    except Exception as e:
        print(f"Exception occurred in alert_new_demon: {e}")


# Pushover GUI
def open_pushover_gui():
    print("Opening Pushover GUI")
    try:
        load_config('pushover')
        pushover_gui.clear()
        pushover_gui.addLabel("<h2 style='color:#bd93f9'>Pushover Configuration</h2>")
        pushover_gui.addLabel("<span style='color:#71e0cb'>Pushover User Key:</span>")
        pushover_gui.addLineedit(pushover_config['user_key'], set_pushover_user_key)
        pushover_gui.addLabel("<span style='color:#71e0cb'>Pushover API Token:</span>")
        pushover_gui.addLineedit(pushover_config['api_token'], set_pushover_api_token)
        pushover_gui.addButton("Save Configuration", save_pushover_config)
        pushover_gui.setSmallTab()
    except Exception as e:
        print(f"Exception occurred while setting up Pushover GUI: {e}")

def set_pushover_user_key(text):
    print(f"Setting Pushover user key: {text}")
    pushover_config['user_key'] = text

def set_pushover_api_token(text):
    print(f"Setting Pushover API token: {text}")
    pushover_config['api_token'] = text

def save_pushover_config():
    print("Saving Pushover config")
    save_config('pushover')
# Teams GUI
def open_teams_gui():
    print("Opening Teams GUI")
    try:
        load_config('teams')
        teams_gui.clear()
        teams_gui.addLabel("<h2 style='color:#bd93f9'>Teams Configuration</h2>")
        teams_gui.addLabel("<span style='color:#71e0cb'>Teams Webhook URL:</span>")
        teams_gui.addLineedit(teams_config['webhook_url'], set_teams_webhook_url)
        teams_gui.addButton("Save Configuration", save_teams_config)
        teams_gui.setSmallTab()
        print("Teams GUI setup complete")
    except Exception as e:
        print(f"Exception occurred while setting up Teams GUI: {e}")

def set_teams_webhook_url(text):
    print(f"Setting Teams webhook URL: {text}")
    teams_config['webhook_url'] = text

def save_teams_config():
    print("Saving Teams config")
    save_config('teams')


# Options GUI
def open_options_gui():
    print("Opening Options GUI")
    try:
        options_gui.clear()
        options_gui.addLabel("<h3 style='color:#bd93f9'>Options</h3>")
        #options_gui.addCheckbox("Save keys to file", toggle_save_keys, save_keys)
        options_gui.addCheckbox("Send Listener", toggle_send_listener, send_listener)
        options_gui.addCheckbox("Send External IP", toggle_send_external_ip, send_external_ip)
        options_gui.addCheckbox("Send Internal IP", toggle_send_internal_ip, send_internal_ip)
        options_gui.addCheckbox("Send Username", toggle_send_username, send_username)
        options_gui.addCheckbox("Send Hostname", toggle_send_hostname, send_hostname)
        options_gui.addCheckbox("Send Domain", toggle_send_domain, send_domain)
        options_gui.addCheckbox("Send OS", toggle_send_os, send_os)
        options_gui.addCheckbox("Send OS Build", toggle_send_os_build, send_os_build)
        options_gui.addCheckbox("Send OS Architecture", toggle_send_os_arch, send_os_arch)
        options_gui.addCheckbox("Send Process Name", toggle_send_process_name, send_process_name)
        options_gui.addCheckbox("Send Process ID", toggle_send_process_id, send_process_id)
        options_gui.addCheckbox("Send Process Architecture", toggle_send_process_arch, send_process_arch)
        options_gui.setSmallTab()
    except Exception as e:
        print(f"Exception occurred while setting up Options GUI: {e}")
def toggle_save_keys():
    global save_keys
    save_keys = not save_keys
    save_options()
    print(f"Toggled save_keys to {save_keys}")

def toggle_send_listener():
    global send_listener
    send_listener = not send_listener
    save_options()
    print(f"Toggled send_listener to {send_listener}")

def toggle_send_external_ip():
    global send_external_ip
    send_external_ip = not send_external_ip
    save_options()
    print(f"Toggled send_external_ip to {send_external_ip}")

def toggle_send_internal_ip():
    global send_internal_ip
    send_internal_ip = not send_internal_ip
    save_options()
    print(f"Toggled send_internal_ip to {send_internal_ip}")

def toggle_send_username():
    global send_username
    send_username = not send_username
    save_options()
    print(f"Toggled send_username to {send_username}")

def toggle_send_hostname():
    global send_hostname
    send_hostname = not send_hostname
    save_options()
    print(f"Toggled send_hostname to {send_hostname}")

def toggle_send_domain():
    global send_domain
    send_domain = not send_domain
    save_options()
    print(f"Toggled send_domain to {send_domain}")

def toggle_send_os():
    global send_os
    send_os = not send_os
    save_options()
    print(f"Toggled send_os to {send_os}")

def toggle_send_os_build():
    global send_os_build
    send_os_build = not send_os_build
    save_options()
    print(f"Toggled send_os_build to {send_os_build}")

def toggle_send_os_arch():
    global send_os_arch
    send_os_arch = not send_os_arch
    save_options()
    print(f"Toggled send_os_arch to {send_os_arch}")

def toggle_send_process_name():
    global send_process_name
    send_process_name = not send_process_name
    save_options()
    print(f"Toggled send_process_name to {send_process_name}")

def toggle_send_process_id():
    global send_process_id
    send_process_id = not send_process_id
    save_options()
    print(f"Toggled send_process_id to {send_process_id}")

def toggle_send_process_arch():
    global send_process_arch
    send_process_arch = not send_process_arch
    save_options()
    print(f"Toggled send_process_arch to {send_process_arch}")


# Load configuration for Pushover and Teams
def load_all_configs():
    load_config('pushover')
    load_config('teams')

# Save configuration for Pushover and Teams
def save_all_configs():
    save_config('pushover')
    save_config('teams')

# Function to send notifications based on configuration
def send_notification(message):
    if pushover_config['user_key'] and pushover_config['api_token']:
        send_pushover_notification(message)
    if teams_config['webhook_url']:
        send_teams_notification(message)

# Load all configurations
load_all_configs()
load_notified_demons()
load_options()

# Initialize GUI
pushover_gui = havocui.Widget("Pushover Configuration", True)
teams_gui = havocui.Widget("Teams Configuration", True)
options_gui = havocui.Widget("Options", True)

# Create GUI tabs
try:
    havocui.createtab("Notifications", "Pushover", open_pushover_gui, "Teams", open_teams_gui, "Options", open_options_gui)
except Exception as e:
    print(f"Exception occurred while creating GUI tabs: {e}")

# Set up event monitoring
event = Event("events")
event.OnNewSession(alert_new_demon)
