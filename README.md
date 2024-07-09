
## Features

- Send notifications to Pushover and Microsoft Teams when a new daemon connects.
- Configure Pushover user key and API token.
- Configure Microsoft Teams webhook URL.
- Select which daemon information to include in the notification.
- Save configuration settings to a file.

## Installation
1. Install required dependencies:
    ```bash
    pip install requests
    ```
2. Download the file, and open with script-manager
    

## Usage

1. **Load the script in Havoc C2:**
   - Open the Havoc C2 client.
   - Navigate to `Scripts > Scripts Manager > Load Script`.
   - Select the `Havoc_pushover.py` script and load it.

2. **Configure Pushover:**
   - Navigate to `Notifications > Pushover`.
   - Enter your Pushover user key and API token.
   - Click "Save Configuration".

![bilde](https://github.com/2spentest/Havoc_notify/assets/6630936/aa3ba155-5959-4af5-9490-a6098646cb22)



3. **Configure Microsoft Teams:**
   - Navigate to `Notifications > Teams`.
   - Enter your Microsoft Teams Webhook URL.
   - Click "Save Configuration".
  
 ![bilde](https://github.com/2spentest/Havoc_notify/assets/6630936/0c2e1659-fe20-4d0a-b16b-da35b72e5f6a)

4. **Set Notification Options:**
   - Navigate to `Notifications > Options`.
   - Select which daemon information to include in the notification by checking the corresponding boxes.
   - Click "Save Options".

![bilde](https://github.com/2spentest/Havoc_notify/assets/6630936/fbe50cac-b3d5-4ce4-ba71-b28af37276f0)



## Microsoft Teams Workflow

To create a workflow in Microsoft Teams to receive notifications:

1. Visit the [Power Automate template](https://make.preview.powerautomate.com/galleries/public/templates/d271a6f01c2545a28348d8f2cddf4c8f/post-to-a-channel-when-a-webhook-request-is-received).
2. Follow the instructions to set up a new workflow that posts to a channel when a webhook request is received.
3. Copy the webhook URL provided by the workflow.
4. Enter this webhook URL in the Teams configuration section of the Havoc C2 script.

For detailed instructions on creating an incoming webhook in Microsoft Teams, refer to the [official Microsoft Teams documentation](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook?tabs=newteams%2Cdotnet#create-an-incoming-webhook).

## Example Notification

The notification message includes details such as Listener, External IP, Internal IP, Username, Hostname, Domain, OS, OS Build, OS Architecture, Process Name, Process ID, and Process Architecture.

![bilde](https://github.com/2spentest/Havoc_notify/assets/6630936/ce5af6d7-3b42-4a56-8645-528bbaeedb6e)

