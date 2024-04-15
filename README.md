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
