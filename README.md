# dsci551-project
Ensure the python version is 3.8/3.9.

Commands to run the project:


# Create virtual Environment
```bash 
python3 -m venv venv
```
# Use venv

```bash
source venv/bin/activate
```
# Install required dependencies (Make sure mongodb is already installed)
```bash
pip3 install django django-extensions djongo pytz
pip install pymongo==3.12.3
```

# Initilaize DBs and import data
```bash
cd health_insights
```
```bash
python3 manage.py makemigrations
  ```
```bash
python3 manage.py migrate
  ```
```bash
python3 manage.py runscript parser2
```
# To run the app

```bash
python3 manage.py runserver
```



# File Structure
health_insights:

Urls.py: This file contains the URLs of the pages we've created.
Settings.py: It's the default configuration file for the Django project, where we configure our apps and databases.

insights:

Templates/insights: This directory houses all our HTML templates.
Models.py: Here, we define our database models.
init.py: This file makes Python treat the directories as containing packages; it can be empty.
admin.py: Used to register models for Django's admin interface.
apps.py: Contains settings for application configuration.
forms.py: Defines forms for the application, extending Django's form functionality for templates.
router.py: Manages database routing for multiple databases.
tests.py: Contains test classes and functions to run against the application.
views.py: Contains the logic and control flow for handling requests, defining functions and classes to manage data presentation.
```
