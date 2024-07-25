import vimeo
import os
import glob
from datetime import datetime

client = vimeo.VimeoClient(
    token='YOUR-TOKEN',
    key='YOUR-KEY',
    secret='YOUR-SECRET'
)

def get_latest_file(folder_path):
    list_of_files = glob.glob(f'{folder_path}/*.mp4')
    return max(list_of_files, key=os.path.getctime)

def upload_to_vimeo(file_path):
    try:
        title = f"Video Upload {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        uri = client.upload(file_path, data={
            'name': title,
            'description': 'Uploaded via API'
        })
        return client.get(uri + '?fields=link').json()['link']
    except vimeo.exceptions.VimeoUploadException as e:
        print('Error uploading')
        print('Server reported: {0}'.format(e.message))
    except vimeo.exceptions.VimeoException as e:
        print('Error making API call')
        print('Server reported: {0}'.format(e.message))

if __name__ == "__main__":
    folder_path = r"C:\Users\YOUR-FILEPATH"
    latest_file = get_latest_file(folder_path)
    video_link = upload_to_vimeo(latest_file)
    print(f"Uploaded file: {latest_file}")
    print(f"Vimeo link: {video_link}")
