from __future__ import print_function
from ast import Import

import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

with open(r'C:\Users\Pedro\Desktop\Estudos\Python\Projetos\AutoDriveBackup\configs.json') as Jarchive:
    data = dict(json.load(Jarchive))

    local_folder_path = os.path.normpath(data['local_folder_path'])
    drive_folder_id = data['driver_folder_id']

    print("local_folder_path:",local_folder_path)
    print("drive_folder_id:",drive_folder_id)


class AutoDriveBackup(): 
    def __init__(self):
        try:
            self.creds = None

            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)

            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        r'C:\Users\Pedro\Desktop\Estudos\Python\Projetos\AutoDriveBackup\credentials.json', SCOPES)
                    self.creds = flow.run_local_server(port=0)

                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())
            self.service = build('drive', 'v3', credentials=self.creds)
        except:
            print("Error in init AutoDriveBackup")

    def FileList(self):
        files = []
        for file_name in os.listdir(local_folder_path):
            file_metadata = {'name': file_name, 'parents': [drive_folder_id]}
            media = MediaFileUpload(f'{local_folder_path}//{file_name}')
            files.append((file_metadata,media))
        return files


    def UploadFile(self, file_metadata, media):
        try:
            self.service.files().create(body=file_metadata, media_body=media).execute()
            print(f"Archive upload successfully ({file_metadata['name']})")
        except:
            print(f"Error to upload the file '{file_metadata['name']}'")
    
if __name__ == '__main__':
    ADB = AutoDriveBackup()
    files = ADB.FileList()
    t = 'asdasdasd'
    ADB.UploadFile(file_metadata=files[0][0], media=files[0][1])
