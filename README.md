# Google Drive Manager

This project contains a Python script `google_drive_manager.py` that manages Google Drive files. It uses the Google Drive API to authenticate, list, and manage files.

## Installation

To install the necessary dependencies, run the following command:

```bash
pip install oauth2client pydrive
```

## Google Service Credentials

To use this script, you'll need to obtain service credentials from Google. Here's how you can do it:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).

2. Create a new project or select an existing one.

3. In the sidebar on the left, go to APIs & Services > Library.

4. Search for 'Google Drive API', select the entry, and click 'ENABLE'.

5. Go to APIs & Services > Credentials.

6. Click on 'Create Credentials' and select 'Service account'.

7. Follow the prompts to create a new service account and download the JSON file.

8. Rename the downloaded JSON file to 'Service_credentials.json' and place it in the 'credentials' directory of this project.

## Usage

To use the script, simply run:

```
python google_drive_manager.py
```

> Please note that the script assumes the 'Service_credentials.json' file is located in a 'credentials' directory at the same level as the script itself.

