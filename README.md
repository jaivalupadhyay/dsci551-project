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

### health_insights
- **Urls.py**: Contains the URLs of the pages created for the application.
- **Settings.py**: Default configuration file for the Django project, handling app and database configurations.
- - **init.py**: Makes Python treat the directory as containing packages.

### insights
- **Templates/insights**: Directory containing HTML templates.
- **Models.py**: Defines database models.
- **init.py**: Makes Python treat the directory as containing packages.
- **admin.py**: Registers models for Django's admin interface.
- **apps.py**: Contains application-specific configuration settings.
- **forms.py**: Defines forms for the application.
- **router.py**: Manages database routing for multiple databases.
- **tests.py**: Contains test classes and functions.
- **views.py**: Handles request logic and data presentation.

- ### Parser
- **parser2.py**: Used to parse and load the initial data into the web application.


