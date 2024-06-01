import plaid
from plaid.api import plaid_api
from django.conf import settings
import json

def pretty_print_response(response):
    print(json.dumps(response, indent=2, sort_keys=True, default=str))


def format_error(e):
    response = json.loads(e.body)
    return {
        "error": {
            "status_code": e.status,
            "display_message": response["error_message"],
            "error_code": response["error_code"],
            "error_type": response["error_type"],
        }
    }


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
