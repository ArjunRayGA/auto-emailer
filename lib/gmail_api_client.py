import os
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = '../client_secret.json'
APPLICATION_NAME = 'Auto-Mailer'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_client():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)    
    return service

def test_client(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])

import markdown as md

def markdown_compiler(body, **kwargs):
    body_path = os.path.join(os.getcwd(), body)
    print body_path, kwargs
    md_file = open(body)
    print md_file
    return False
    

def markdown_to_html(md_text):
    html = md.markdown(md_text)
    return html
# def message
#     message = CreateMessage('deconstructionalism@gmail.com', 'aray@brandeis.edu', 'arjun.ray@generalassemb.ly', 'arjun_ray@brown.edu', "test message", message)
#     SendMessage(service, 'me', message)

import base64
from email.mime.text import MIMEText
from apiclient import errors

def send_message(service, user_id, message):

  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError:
    print('An error occurred: %s' % error)


def create_message(sender, to, cc, bcc, subject, message_text):
  message = MIMEText(message_text, 'html')
  message['to'] = to
  message['from'] = sender
  message['cc'] = cc
  message['bcc'] =  bcc
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

