# Steps:
# 1. Download credentials.json from https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the and put to this folder
# 2. Run python start.py

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from colored import fg, attr

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/drive.file']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    files = service.files().list(
        pageSize=1000, fields="files(id, name, modifiedByMeTime, capabilities, webViewLink, owners, trashed)", orderBy='modifiedByMeTime desc', corpora='user').execute()
    files = files.get('files', [])

    if not files:
        print('No files found.')
    else:
        for file in files:
            # If it's a Google Document that was commented/edited by me
            if file.get('capabilities').get('canComment') and file.get('modifiedByMeTime') and "docs.google.com/document/" in file['webViewLink'] and not file.get('trashed'):
                try:
                    # Get comments with author and content
                    comments = service.comments().list(
                        fileId=file['id'], fields="comments(author,content)", pageSize=100).execute().get('comments', [])
                    myComments = []
                    for comment in comments:
                        if comment['author']['me']:
                            # Check for my comment
                            myComments.append(comment['content'])
                    if myComments:
                        print(u'\nFile Name: {0}'.format(file['name']))
                        print(u'File Owner: {0}'.format(
                            file['owners'][0]['displayName']))
                        print(u'File URL: {0}'.format(file['webViewLink']))
                        for comment in myComments:
                            print(fg('green') + '• ' + comment + attr('reset'))
                except Exception as e:
                    print(file)
                    print(u'\nFile Name: {0}'.format(file['name']))
                    print(u'File Owner: {0}'.format(
                        file['owners'][0]['displayName']))
                    print(u'File URL: {0}'.format(file['webViewLink']))
                    print(fg('red'), 'Unexpected error: ', e, attr('reset'))


if __name__ == '__main__':
    main()
