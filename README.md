# dsci551-project

Commands to run the project:
# Use venv if exists

source venv/bin/activate

# Initilaize DBs and import data

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py parser2

# To run the app

python3 manage.py runserver
