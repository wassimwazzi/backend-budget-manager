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

## Huey
1- Run the consumer
```bash
python manage.py run_huey
```


