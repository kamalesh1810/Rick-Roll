import os
from email.mime.image import MIMEImage
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# getting credentials
CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

# creating service for using gmail API
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# the host url will be the url returned after hosting the app in aws beanstalk
HOST_URL=os.getenv('HOST_URL')


# function to send the initail set of e-mail to the users
def mail(email,name):
    try:
        # this contains the email body in html format
        emailMsg = f'''<body>
        Dear Student,<br><br>
        The final semester results have been announced for CSE Department.<br>
        Students with overall CGPA more than 8.0 are eligible for a scholarship and are requested to fill the attached form immediately.<br><br>
        <a href="{HOST_URL}/?email={email}">https://docs.google.com/forms/wxed...</a><br><br><br>
        Thanks and Regards,<br>
        CSE Dept<br>
        <img src="cid:image1">
        <body>
        '''
        
        # gmail-is used to send out the e-mails
        sender_email = ''

        # name of sender
        sender_name = ''

        mimeMessage = MIMEMultipart()
        mimeMessage['from'] = f'{sender_name} <{sender_email}>'
        mimeMessage['to'] = f'{email}'

        # mail subject
        mimeMessage['subject'] = f'{name}, Fill Important Details!'
        mimeMessage.attach(MIMEText(emailMsg, 'html'))

        # yuo can also add an additional image to the mail
        fp = open('attachment_image.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image1>')
        mimeMessage.attach(msgImage)

        # send mail using gmail API
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print(message)

    except Exception as e:
        print(e)
        pass

# open the csv which contains user names and e-mail ids
df = pd.read_csv('users_list.csv')

emails = df['email'].tolist()
names = df['name'].tolist()

# loop to send mail
count=0
for email in emails:
    mail(email, names[count])
    count+=1