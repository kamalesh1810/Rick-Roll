from flask import Flask, render_template, request
import os
import firebase_functions
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# getting credentials
CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

# the host url will be the url returned after hosting the app in aws beanstalk
HOST_URL = os.getenv('HOST_URL')

# creating service for using gmail API
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# function to send a mail to a user who has been rick rolled
def mail(email,name):
    try:
        emailMsg = f'''<body>
        Good Job {name},<br><br>
        You have been successfully rick-rolled!!.<br>
        Click the below link to view the wall of fame. If you don't want to be the only one on it, please refrain from informing it to your friends.<br><br>
        <a href="{HOST_URL}/list">Hall of Fame</a><br><br><br>
        Thanks and Regards,<br>
        CSE Dept<br>
        <body>
        '''

        # gmail-id used to send out the e-mails
        sender_email = ''
        # name of sender
        sender_name = ''

        mimeMessage = MIMEMultipart()
        mimeMessage['from'] = f'{sender_name} <{sender_email}>'
        mimeMessage['to'] = f'{email}'
        mimeMessage['subject'] = f"Congrats! You've been rolled!"
        mimeMessage.attach(MIMEText(emailMsg, 'html'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        message = service.users().messages().send(userId = 'me', body = {'raw': raw_string}).execute()
        print(message)

    except Exception as e:
        print(e)
        pass


app = Flask(__name__)

# base url which will redirect the user to the youtube video
@app.route('/')
def index():
    # the email-id is embedded as a query parameter
    email = request.args.get('email')

    # checking if the email-id exists in firebase
    if firebase_functions.doc_exists(email):

        # check if the second mail is sent to the user, just in case they open the link again
        mail_sent = firebase_functions.get_field('mail_sent',email)   

        # if mail is not sent to the particular email-id
        if mail_sent is None: 

            # get the corresponding name from firebase
            user_name = firebase_functions.get_field('name',email)

            # send second mail to user
            mail(email,user_name)

            # set mail_sent flag to true, and add the user name to the rick rolled list
            firebase_functions.set_field('mail_sent',True,email)
            firebase_functions.add_to_rolled_list(user_name)
        
        # rendering the index.html template which redirects users to the youtube video in all cases
        else:
            return render_template('index.html')
    else: 
        return render_template('index.html')
    return render_template('index.html')

# endpoint to show all the user names in the Hall of Fame
@app.route('/list')
def list_users():
    # get list of rick rolled users from firebase
    rick_rolled_students_list = firebase_functions.get_rolled_list()
    return render_template('lists.html', data = rick_rolled_students_list, count = len(rick_rolled_students_list))
    
if __name__ == '__main__':
	app.run(debug = True, host = "0.0.0.0", port = int(os.environ.get("PORT", 8080)))
