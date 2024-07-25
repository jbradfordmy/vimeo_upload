import vimeo
import os
import time
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Vimeo setup
client = vimeo.VimeoClient(
    token='YOUR_VIMEO_ACCESS_TOKEN',
    key='YOUR_VIMEO_API_KEY',
    secret='YOUR_VIMEO_API_SECRET'
)

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = r'PATH_TO_YOUR_GOOGLE_SERVICE_ACCOUNT_JSON_FILE'
SPREADSHEET_ID = 'YOUR_GOOGLE_SPREADSHEET_ID'
RANGE_NAME = 'Sheet1!A:B'  # Adjust as needed

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=creds)

def upload_to_vimeo(file_path, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            title = f"Video Upload {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            uri = client.upload(file_path, data={
                'name': title,
                'description': 'Uploaded via API'
            })
            return client.get(uri + '?fields=link').json()['link']
        except Exception as e:
            print(f'Error uploading to Vimeo (Attempt {attempt + 1}/{max_retries})')
            print(f'Error: {str(e)}')
            if attempt < max_retries - 1:
                print(f'Retrying in {delay} seconds...')
                time.sleep(delay)
            else:
                print('Max retries reached. Upload failed.')
                return None

def update_google_sheet(title, link):
    try:
        values = [[title, link]]
        body = {'values': values}
        result = sheets_service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
    except Exception as e:
        print('Error updating Google Sheet')
        print('Error: {0}'.format(str(e)))

class NewVideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.mp4'):
            print(f"New video detected: {event.src_path}")
            # Add a short delay to ensure the file is fully written
            time.sleep(5)
            video_link = upload_to_vimeo(event.src_path)
            if video_link:
                print(f"Uploaded file: {event.src_path}")
                print(f"Vimeo link: {video_link}")
                title = os.path.basename(event.src_path)
                update_google_sheet(title, video_link)
            else:
                print("Upload failed. Please check the error messages above.")

if __name__ == "__main__":
    folder_to_watch = r"PATH_TO_YOUR_STREAMYARD_DOWNLOAD_FOLDER"
    event_handler = NewVideoHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()
    print(f"Watching for new videos in {folder_to_watch}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
