#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by Raymond Aarseth and Sopra Steria Norway
# Description:
#  A script to send Pushover notifications for new daemon connections in Havoc C2
#  with a GUI for inserting Pushover keys.
# Usage:
#  To use this script save it on your machine and add it to the script manager of Havoc
#  inside of: Scripts > Scripts Manager > Load Script

import requests
import havocui
from havoc import Demon, RegisterCallback, Event

# Global variables for Pushover keys
pushover_user_key = ""
pushover_api_token = ""

# Function to send a Pushover notification
def send_pushover_notification(message):
    payload = {
        'token': pushover_api_token,
        'user': pushover_user_key,
        'message': message
    }
    response = requests.post('https://api.pushover.net/1/messages.json', data=payload)
    if response.status_code == 200:
        print('Notification sent successfully.')
    else:
        print(f'Failed to send notification. Status code: {response.status_code}')

# Callback function for new daemon connections
def alert_new_demon(demonID):
    # This function is called when a new daemon connects
    demon = Demon(demonID)

    # Collect some basic info about this new daemon
    info = {
        'id': demonID,
        'arch': demon.ProcessArch,
        'user': demon.User,
        'hostname': demon.Computer,
        'ip': demon.InternalIP
    }

    # Create a message for the Pushover notification
    message = (f"New daemon connected:\n"
               f"ID: {info['id']}\n"
               f"Arch: {info['arch']}\n"
               f"User: {info['user']}\n"
               f"Hostname: {info['hostname']}\n"
               f"IP: {info['ip']}")

    # Send the Pushover notification
    send_pushover_notification(message)

# GUI to input Pushover keys
def open_pushover_gui():
    pushover_gui.clear()
    pushover_gui.addLabel("<h3 style='color:#bd93f9'>Pushover Configuration</h3>")
    pushover_gui.addLabel("<span style='color:#71e0cb'>Pushover User Key:</span>")
    pushover_gui.addLineedit(pushover_user_key, set_user_key)
    pushover_gui.addLabel("<span style='color:#71e0cb'>Pushover API Token:</span>")
    pushover_gui.addLineedit(pushover_api_token, set_api_token)
    pushover_gui.addButton("Save and Start", save_keys_and_start)
    pushover_gui.setSmallTab()

# Set Pushover User Key
def set_user_key(text):
    global pushover_user_key
    pushover_user_key = text

# Set Pushover API Token
def set_api_token(text):
    global pushover_api_token
    pushover_api_token = text

# Save keys and start monitoring
def save_keys_and_start():
    if not pushover_user_key or not pushover_api_token:
        havocui.errormessage("Please enter both the Pushover User Key and API Token.")
    else:
        event = Event("events")
        event.OnNewSession(alert_new_demon)
        print("Pushover keys saved and script started.")

# Create Pushover GUI tab
pushover_gui = havocui.Widget("Pushover Configuration", True)
havocui.createtab("Pushover Config", "Pushover", open_pushover_gui)

