# Setup
## Venv
1- Create a virtual environment
```bash
python -m venv venv
```
2- Activate the virtual environment
```bash
source venv/bin/activate
```
3- Install the requirements
```bash
pip install -r requirements.txt
```
4- Run the server
```bash
python manage.py runserver
```

## Database
1- Create the migrations
```bash
python manage.py make migrations
```
2- Apply the migrations
```bash
python manage.py migrate
```
3- Create a superuser
```bash
python manage.py createsuperuser
```

## Celery
1- Install Redis
```bash
sudo apt-get install redis-server
```
OR on Mac
```bash
brew install redis
```
2- Run the server
```bash
redis-server
```
3- Run Celery
```bash
celery -A backend worker -l info
```


