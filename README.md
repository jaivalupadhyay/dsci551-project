# dsci551-project

Commands to run the project:


# Create virtual Env
```bash 
python3 -m venv venv
```
# Use venv

```bash
source venv/bin/activate
```
# Install required dependiencies
```bash
pip3 install -r requirements.txt
```
# Initilaize DBs and import data

```bash
   python3 manage.py makemigrations
  ```
```bash
  python3 manage.py migrate
  ```
```bash
  python3 manage.py parser2
```
# To run the app

```bash
python3 manage.py runserver
```
