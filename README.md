# nuze
A news site using the Flask framework

# Setup
Create a virtual environment to store the python extensions  
$ `python -m venv .venv`

Activate the virtual environment:  
$ `source .venv/bin/activate`

### Install the required extensions from the requirements.txt file
$ `pip install -r requirements.txt`

### Environment Variables
Use the .env file to set the environment variables. When the app is run, the environment varibles are loaded from the .env file using python-dotenv. If no values are supplied, the app is configured from default variables specified in config.py. You do not need to set any environment variables to run the app, but you will need to set the environment variables related to Flask-Mail for the email functionality of the app to work.

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
After you've set the environment variables and created the databse, you can run the site:  
$ `flask --app nuze.py run`

The admin's username is admin and the password is admin

### Utils
The functions in util.py have been added to the client command line. To use them, first make sure the FLASK_APP environment variable is set to nuze.py:  
$`export FLASK_APP=nuze.py`
You can then run the helper function in the command line while the app is not running with:  
$`flask function-name`

The helper functions are:  
$`flask get-users`: list the users in the database  
$`flask get-env`: list the environment variables  
$`flask get-urls`: list the url_map (all routes in app)  
$`flask make-key`: create a key that can be pasted into .env as a secret key  

### Protect against Open Redirects
In auth/views.py there is a view for logging in users. If a user is not logged in and they try to access a page that requires they be logged in, they will be redirected to the login page and the page they first tried to access will be passed along as the 'next' arguement. After they log in, the 'next' url they requested will be checked to see if it is safe if in is_safe_url. This checks the 'next' url to see if it is in the same domain as any url in the SAFE_URLS variable. By default, SAFE_URLS is set to a list of the routes in this site that can be obtained with:  
$`flask get-urls`  
you can also set the SAFE_URLS evironment variable in .env, but be sure to add the internal routes from this site as well.