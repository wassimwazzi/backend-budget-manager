import plaid
from plaid.api import plaid_api
from django.conf import settings


def get_plaid_env():
    if settings.PLAID_ENV.lower() == "sandbox":
        return plaid.Environment.Sandbox
    if settings.PLAID_ENV.lower() == "development":
        return plaid.Environment.Development
    if settings.PLAID_ENV.lower() == "production":
        return plaid.Environment.Production
    return plaid.Environment.Sandbox

configuration = plaid.Configuration(
    host=get_plaid_env(),
    api_key={
        "clientId": settings.PLAID_CLIENT_ID,
        "secret": settings.PLAID_SECRET,
    },
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)
