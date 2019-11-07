#! /usr/bin/python
#-*- coding: Utf-8 -*-
from __future__ import print_function
import httplib2
import sys
import os
import io

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument("fichier", help="Nom de fichier a transferer")
    flags = parser.parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.file'

CLIENT_SECRET_FILE = 'gdrive_client_secret.json'
CREDENTIAL_FILE = 'drive-python-drivejce.json'
APPLICATION_NAME = 'SAS DRIVEJCE'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                CREDENTIAL_FILE)

    client_secret_path = os.path.join(credential_dir,
                                CLIENT_SECRET_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_parent_id(s, name):
    query='name="'+name+'"'
    results = s.files().list(q=query,fields="files(id)").execute()
    items = results.get('files', [])
    id=None
    if len(items) > 0:
        id=items[0]['id']
    return id
    
def prompt(max):
    while True:
        print ("no / <CR> (suite) / 0|q (quit)"); r=raw_input("?")
        try :
            no=int(r)
            if no <= max:
                return no
        except:
            pass
        if r=='':
            return -1
        if r.upper()=='Q':
           return 0


def file_down(s, i):
    file_id=i["id"]
    file_name=i["name"]
    request = s.files().get_media(fileId=file_id)
    f=open(file_name,"w")    
    downloader = MediaIoBaseDownload(f, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    f.close()

def main(file_path):
    credentials = get_credentials()
    print(credentials)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    sas_folder="SAS"
    parent_id=get_parent_id(service,sas_folder)
    if not parent_id:
        print("Pas de repertoire "+sas_folder)    
        # return(1)
    print("parent_id",parent_id)


    meta_data={'name': file_path, "parents": [parent_id] }

    print("upload...")
    parent=[parent_id]
    results = service.files().create(body=meta_data,media_body=file_path,fields='id').execute()

    print(results)

if __name__ == '__main__':
    if len(sys.argv) != 2 :
        print("fichier argument manquant")
        sys.exit(1)
    file_path=sys.argv[1]
    try:
        with open(file_path) as f: pass
    except IOError as e:
        print(e)
        sys.exit(2)
    f.close()

    main(file_path)
