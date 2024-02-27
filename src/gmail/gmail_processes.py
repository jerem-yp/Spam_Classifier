""" Functions to access Gmail API. """
import configparser
import os
import pickle

# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Documentation
from typing import List

def _gmail_authenticate(scopes: List[str], pickle_path: os.path, secrets_path: os.path):
    creds = None

    # If already authenticated, no need to do it again
    if os.path.exists(pickle_path):
        with open(pickle_path, "rb") as token:
            creds = pickle.load(token)

    if creds is None or not creds.valid:
        if creds is not None and creds.expired and creds.refresh_token:
            creds.refresh(Request()) # Request a new token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secrets_path, scopes = scopes)
            creds = flow.run_local_server(port=0)

        with open(pickle_path, "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

def _read_message(gService, message) -> dict:
    """ Will download and read the message.
    :params
     gService: Service (from gmail_authenticate)
     message: single Message object
    :return None, as this prints everything out
    """
    msg = gService.users().messages().get(userId='me', id=message['id'], format='full').execute()

    #Now parse the message
    payload = msg['payload']
    headers = payload.get('headers')

    data = {}
    if headers: # To/From/Subject/Date
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'to':
                data['to'] = value
            elif name.lower() == 'from':
                data['from'] = value
            elif name.lower() == 'subject':
                data['subject'] = value
            elif name.lower() == 'date':
                data['date'] = value

    return data

def _search_messages(service):
    """ Fetch a page of results. Fetches one page at a time. """
    result = service.users().messages().list(userId='me').execute()
    messages = []
    if 'messages' in result:
        messages.extend(result['messages'])
    yield messages

def getResults(init_fp: os.path, pickle_path: os.path, secret_path: os.path) -> List[dict] | None: # API-callable function
    """ Use the configparser to get the correct data. Throws KeyError if key DNE, and
    FileNotFound error if file does not exist.
    :param init_fp: Path to INI file in init/
    :return dictionary if worked correctly, None if else"""
    config = configparser.ConfigParser()

    if not os.path.exists(init_fp):
        raise FileNotFoundError(f"File {init_fp} does not exist.")

    config.read(init_fp)
    try:
        email = config["AUTH"]["email"]
        if not email:
            raise NotImplementedError
    except KeyError:
        print("Section 'AUTH' key 'email' does not exist.")
        return None
    except NotImplementedError:
        print("Section 'AUTH' key 'email' is empty.")
        return None

    scopes = []
    try:
        scope = config["AUTH"]["scope"]
        if not scope:
            raise NotImplementedError
        else:
            scopes.append(scope)
    except KeyError:
        print("Section 'AUTH' key 'email' does not exist.")
        return None
    except NotImplementedError:
        print("Section 'AUTH' key 'scope' is empty.")
        return None

    gService = _gmail_authenticate(scopes=scopes, pickle_path=pickle_path, secrets_path = secret_path)

    messageDict = []
    for messageGroup in _search_messages(gService):
        for message in messageGroup: # Single message
            messageDict.append(_read_message(gService, message))

        yield messageDict
        messageDict = [] # Reset


