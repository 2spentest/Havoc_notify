# Pushover Notification Script for Havoc C2

This Python script integrates with the Havoc C2 framework to send Pushover notifications for new daemon connections. It includes a GUI for configuring Pushover keys and selecting which daemon attributes to include in notifications.

## Features
- **Notification Settings**: Configure which daemon details (Listener, IP addresses, username, hostname, etc.) to include in notifications.
- **Pushover Integration**: Easily set and save Pushover User Key and API Token through the GUI.
- **Not so secure key storage**: Keys are saved in ~/.config in clear text and should not be used unless you really need to and know the risk. you have been warned. 

![bilde](https://github.com/2spentest/Havoc_pushover/assets/6630936/21a20af1-ecee-47e4-8669-ea0a72322535)


## Usage
1. To use this script, save it on your machine and add it to the script manager of Havoc inside:
**Scripts > Scripts Manager > Load Script**
2. open the Pushover config pane, and insert keys and select options
3. Save and run
4. get notifications

## Installation
1. Install required dependencies:
    ```bash
    pip install requests
    ```
2. Place the script on the machine and open it using the Havoc C2 Scripts Manager.
