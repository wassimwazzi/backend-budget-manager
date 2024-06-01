# Links

[Frontend](https://budget-manager-frontend-0ec640b5ed51.herokuapp.com/)

[Backend](https://budget-manager-backend-1f09feed9afe.herokuapp.com/)

Or, try it out with [Postman](https://www.postman.com/spaceflight-cosmologist-42752282/workspace/budget-manager/overview)

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

4- Setup the environment variables

```bash
cp .env.sample .env
```

And fill in the values

5- Run the server

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

## Ngrok

To use webhooks setup [ngrok](https://dashboard.ngrok.com/get-started/setup/macos)
Update the plaidItem with the new webhook https://plaid.com/docs/api/items/#itemwebhookupdate when in development using [postman](https://www.postman.com/spaceflight-cosmologist-42752282/workspace/budget-manager/request/31974229-8042885b-7f53-4b3e-828d-82c08c8a4232?tab=body)
