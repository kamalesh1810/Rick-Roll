# Rick-Roll

This repository contains the code which I used to Rick Roll over 200 students of my University.

**Disclaimer**- This demonstration is for educational purposes only. The contents of this repository should not be used to perform any harmful activities.

#### Prerequisites
- Clone the repository into your local system
- Install dependencies using 
``` pip install -r requirements.txt```
- Create a gmail account and a GCP project on the same id.
- Create an Oauth client and generate client secrets file, you can refer [this](https://www.youtube.com/watch?v=6bzzpda63H0&ab_channel=JieJenn) video.
- Add the same gmail id as test user in the OAuth Consent Screen.
- Save the json as `client_secrets.json` into both the folders.
- Create a firestore database and add two collections `users` and `troll` as shown below.
![image](https://user-images.githubusercontent.com/61874657/178149288-973a050f-4c07-4c6f-a429-6ec9d6028c65.png)
- Download the service account key for firestore and save it as `serviceAccountKey.json` into both the folders.


#### Data Cleaning and Upload
- Add the list of names and the corresponding e-mails of users whom you want to troll in `user_data.csv` and then run `data_clean.py`
- This will generate `users_list.csv` file, copy it into the Flask App folder as well.
- Now, to upload this user data to firestore, run `upload_users.py` 

#### Modify and host Flask App
- In `app.py` modify the `emailMsg` variable as per your requirement, and edit the `sender_email` and `sender_name` accordingly.
- Host the Flask app folder on AWS Beanstalk, [here](https://www.youtube.com/watch?v=dhHOzye-Rms&ab_channel=NachiketaHebbar)'s a good tutorial.
- After hosting the Flask app successfully on AWS, copy the server url into the `.env` file of both the folders as `HOST_URL` variable. This link will be embedded in the email message body.
- After modifying the env file, update Beanstalk with new source.

#### Sending out Initial set of e-mails
- In `mail_file.py` modify the `emailMsg` variable as per your requirement, and edit the `sender_email` and `sender_name` accordingly.
- Now you're all set to send out the initial set of e-mails.
- Run the `mail_file.py` and send a mail to another account for testing. The first time, you will be redirected to an external URL, complete that Auth using the e-mail id you added as test user in the OAuth consent screen.
- On successful authentication, you will see that token files will be saved in the current directory.
- Run the file again, but this time for all the users present in `users_list.csv`
- If the script is running successfully, you will be able to see the message printed in the console for each e-mail sent out.
- Now you can just sit back and relax.
- You can open the `/list` endpoint of your aws beanstalk server to see the list of people who have been rick rolled.