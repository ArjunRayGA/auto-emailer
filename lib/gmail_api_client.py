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

def markdown_compiler(body, template_path, **kwargs):
    body_path = os.path.abspath(os.path.join(template_path, body))
    # print body_path, kwargs
    with open(body_path, 'r') as f:
        md_file = f.read()
    print md_file
    return False



def markdown_to_html(md_text):
    html = md.markdown(md_text)
    return html
def test_message():
    message = '''
# ![](..shared/img/header-logo-wide.png)

Hi {{ recipient }},    
    '''
    message = CreateMessage('deconstructionalism@gmail.com', 'aray@brandeis.edu', 'arjun.ray@generalassemb.ly', 'arjun_ray@brown.edu', "test message", message)
    SendMessage(service, 'me', message)

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes

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

def create_message_with_attachment(sender, to, cc, bcc, subject, message_text, file):
  message = MIMEMultipart()
  msg = MIMEText(message_text, 'html')
  message['to'] = to
  message['from'] = sender
  message['cc'] = cc
  message['bcc'] =  bcc
  message['subject'] = subject

  message.attach(msg)

  content_type, encoding = mimetypes.guess_type(file)

  if content_type is None or encoding is not None:
    content_type = 'application/octet-stream'
  main_type, sub_type = content_type.split('/', 1)
  if main_type == 'text':
    fp = open(file, 'rb')
    msg = MIMEText(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'image':
    fp = open(file, 'rb')
    msg = MIMEImage(fp.read(), _subtype=sub_type)
    fp.close()
  elif main_type == 'audio':
    fp = open(file, 'rb')
    msg = MIMEAudio(fp.read(), _subtype=sub_type)
    fp.close()
  else:
    fp = open(file, 'rb')
    msg = MIMEBase(main_type, sub_type)
    msg.set_payload(fp.read())
    fp.close()
  filename = os.path.basename(file)
  msg.add_header('Content-Disposition', 'attachment', filename=filename)
  message.attach(msg)

  return {'raw': base64.urlsafe_b64encode(message.as_string())}