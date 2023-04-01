# nuze
A news site using the Flask framework

# Setup
Create a virtual environment to store the python extensions
$ `virtualenv env`

Activate the virtual environment
$ `source env/Scripts/activate`

### Install the required extensions from the requirements.txt file
$ `pip install -r requirements.txt`

### Environment Variables
You can set environment variables with
$ `export ENV_VAR=value`

This project uses Flask-Mail, so you'll want to set all of the environment variables necessary
to connect to a mail server:
MAIL_SERVER
MAIL_PORT
MAIL_USERNAME
MAIL_PASSWORD
DEFAULT_MAIL_SENDER

You'll also want to set the SECRET_KEY and the WTF_CSRF_SECRET_KEY if deploying in production

### Database
The create_data.py file contains a script that makes a database file with an admin user and 
the basic permissions needed to use the site

Run this script or change it to add other users or permissions

# Run the project
After you've set the environment variables and created the databse, you can run the site
$ `flask --app nuze.py run`

The admin's username is admin and the password is admin
