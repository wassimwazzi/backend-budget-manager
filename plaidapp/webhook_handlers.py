from functools import wraps
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .webhook_handlers import webhook_handlers

webhook_handlers = {}


def register_webhook(event_type):
    def decorator(func):
        webhook_handlers[event_type] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


@register_webhook("SYNC_UPDATES_AVAILABLE")
def handle_sync_updates_available(payload):
    print("SYNC_UPDATES_AVAILABLE")
    print(payload)


# handle plaid webhooks
@csrf_exempt
def handle_webhook(request):
    """
    Handle Plaid webhooks
    """
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method"}, status=405)

    # Retrieve the webhook payload
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Extract event type (assuming it's in the payload, adjust as necessary)
    event_type = payload.get("webhook_code")

    # Process the webhook payload
    handler = webhook_handlers.get(event_type)
    if handler:
        return handler(payload)
    return JsonResponse({"error": "No handler for this event type"}, status=400)
