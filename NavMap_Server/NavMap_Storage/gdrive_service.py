import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import datetime

SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

def get_folder(folder_name):
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = drive_service.files().list(q=query).execute()
    items = response.get('files', [])

    if items:
        return items[0].get('id')
    else:
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = drive_service.files().create(body=file_metadata, fields='id').execute()
        return file.get('id')

def upload_file(file_path, file_name, folder_name):
    media = MediaFileUpload(file_path, resumable=True)
    file_metadata = {
        'name': file_name,
        'parents': [folder_name],
    }
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')