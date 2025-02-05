In these scripts, you'll need to replace the following placeholders with actual values:

  YOUR_VIMEO_ACCESS_TOKEN, YOUR_VIMEO_API_KEY, YOUR_VIMEO_API_SECRET: Your Vimeo API credentials
  PATH_TO_YOUR_GOOGLE_SERVICE_ACCOUNT_JSON_FILE: The path to your Google service account JSON file
  YOUR_GOOGLE_SPREADSHEET_ID: The ID of your Google Sheet
  PATH_TO_YOUR_STREAMYARD_DOWNLOAD_FOLDER: The path to your Streamyard download folder
  PATH_TO_YOUR_PYTHON_EXE: The path to your Python executable
  PATH_TO_YOUR_VIMEO_UPLOAD_SCRIPT: The path to your vimeo_upload.py script

These anonymized files can be safely shared with others. 
Users will need to replace the placeholders with their own information to make the scripts work for their specific setup.

========================================================
Walkthrough for setting up automated Vimeo uploads from a Streamyard download folder with Google Sheets integration:

Set up prerequisites:

  Install Python from python.org
  Create a Vimeo account and get API credentials
  Set up a Google Cloud project and enable Google Sheets API
  Create a Sheets service account and download the JSON key file

Install required Python libraries:
  pip install PyVimeo google-auth-oauthlib google-auth-httplib2 google-api-python-client watchdog

Create a Python script (e.g., vimeo_upload.py) with the following main components:
  Vimeo client setup
  Google Sheets API setup
  Functions for uploading to Vimeo and updating Google Sheets
  A file system event handler to detect new videos
  A main loop to watch the specified folder

Configure the script with your:
  Vimeo API credentials
  Google Sheets service account file path
  Google Sheet ID and range
  Streamyard download folder path

Create a batch file (e.g., run_vimeo_upload.bat) to run the Python script (see the repository)

Run the batch file to start monitoring the folder
(Optional) Add the batch file to Windows startup for automatic execution on system boot

Key features of the script:
  Monitors a specified folder for new .mp4 files
  Automatically uploads new videos to Vimeo
  Updates a Google Sheet with video titles and Vimeo links
  Includes error handling and retry mechanisms

This setup automates the process of uploading Streamyard recordings to Vimeo and logging the links, saving time and reducing manual work.
