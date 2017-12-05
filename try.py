# encoding=utf8  

# from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Auto-Mailer'


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
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        # flow.user_agent = APPLICATION_NAME
        # if flags:
            # credentials = tools.run_flow(flow, store, flags)
        # else: # Needed only for compatibility with Python 2.6
        credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

import markdown
import markdown.extensions.fenced_code

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # results = service.users().labels().list(userId='me').execute()
    results = service.users().drafts().list(userId='me').execute()
    # print(results['drafts'])
    # # labels = results.get('labels', [])

    # for draft in results['drafts']:

    #     message = service.users().messages().get(userId='me', id="152f0bdc49ac4cc2").execute()
    #     print message

    # if not labels:
    #     print('No labels found.')
    # else:
    #   print('Labels:')
    #   for label in labels:
    #     print(label['name'])

    message = markdown.markdown('''
*A method for using `git` to pull changes from our master repo without merge conflicts*

1. You *must* first navigate to the root directory of your local repo copy in your terminal

2. if `git remote -v` doesn’t show remotes with an address `https://github.com/ga-students/DS-BOS-19.git`, run
```git remote add dat-origin https://github.com/ga-students/DS-BOS-19.git```
Otherwise, note the remote name that has the `https://github.com/ga-students/DS-BOS-19.git` address

3. run the following to tell `git pull`/`git merge` to keep local versions of our lesson Jupyter Notebook files, even if they are out of sync with the copies kept in the main repo
```bash
echo 'lessons/**/*.ipynb merge=ours' > .git/info/attributes
```

```bash
git config merge.ours.driver true
```

4. You should be able to run ```git pull <dat-origin / whatever your remote name was from step 2> master``` and pull down changes from the master repo without getting merge conflicts
''', extensions=['fenced_code'])
    print(message)

    message = CreateMessage('deconstructionalism@gmail.com', 'aray@brandeis.edu', 'arjun.ray@generalassemb.ly', 'arjun_ray@brown.edu', "test message", message)

    l = SendMessage(service, 'me', message)
    print(l)

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os

from apiclient import errors


def SendMessage(service, user_id, message):

  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError:
    print('An error occurred: %s' % error)


def CreateMessage(sender, to, cc, bcc, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text, 'html')
  message['to'] = to
  message['from'] = sender
  message['cc'] = cc
  message['bcc'] =  bcc
  message['subject'] = subject
  
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

if __name__ == '__main__':
    main()