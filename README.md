# Rick-Roll

This repository contains the code which I used to Rick Roll over 200 students of my University.

#### Prerequisites
- Clone the repository into your local system
- Install dependencies using 
``` pip install -r requirements.txt```
- Create a gmail account and a GCP project on the same id.
- Create an Oauth client and generate client secrets file, you can refer [this](https://www.youtube.com/watch?v=6bzzpda63H0&ab_channel=JieJenn) video.
- Add the same gmail id as test user in the OAuth Consent Screen.
- Save the json as `client_secrets.json` into both the folders.
- Create a firestore databse and add two collections `users` and `troll` as shown below.
-  

#### Data Cleaning 
- Add the list of names and e-mails 