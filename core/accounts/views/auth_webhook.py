import hashlib
import hmac
import json
import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Organization
from billing.services import create_free_plan_allocation
from config import settings

logger = logging.getLogger(__name__)


@csrf_exempt
def auth_webhook_handler(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON payload
            headers = request.headers
            payload = json.loads(request.body)

            logger.info(f"Received webhook payload: {request.body}")

            secret = settings.WEBHOOK_SECRET_KEY.encode('utf-8')
            received_signature = headers.get("X-Signature")

            # Calculate expected signature
            expected_signature = hmac.new(
                secret,
                request.body,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(expected_signature, received_signature):
                return JsonResponse({"error": "Invalid signature"}, status=401)

            # Check if the type is "user.created"
            if payload.get('type') == 'user.created':
                # Extract the user data from the payload
                user_data = payload.get('data', {})
                user = _user_created_handle(user_data)
                return JsonResponse({"status": "success", "user_id": user.id}, status=201)
            elif payload.get('type') == 'organization.created':
                # Extract the user data from the payload
                org_data = payload.get('data', {})
                org = _organization_created_handle(org_data)
                return JsonResponse({"status": "success", "organization_id": org.id}, status=201)
            else:
                # If the type is not "user.created", just return a success message
                return JsonResponse({"status": "success", "message": "Webhook type not processed"}, status=200)
        except json.JSONDecodeError as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValidationError as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({"error": str(e)}, status=500)
    else:
        # If the HTTP method is not POST, return a 405 Method Not Allowed
        return JsonResponse({"error": "Invalid HTTP method, POST required"}, status=405)


def _user_created_handle(user_data):
    # Check if the necessary fields exist
    email = user_data.get('email')
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    identity_provider_id = user_data.get('id')
    profile_image_url = user_data.get('image')

    if not email:
        return JsonResponse({"error": "Email address is required"}, status=400)

    # Create the user in the database
    user = get_user_model().objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_email_verified=True,
        is_signed_up=True,
        identity_provider_id=identity_provider_id,
        profile_image_url=profile_image_url,
    )
    create_free_plan_allocation(user)
    return user

def _organization_created_handle(org_data):
    # Check if the necessary fields exist
    name = org_data.get('name')
    slug = org_data.get('slug')
    metadata = org_data.get('metadata', {})
    identity_provider_id = org_data.get('id')
    created_by_id = org_data.get('created_by_id')

    user = get_user_model().objects.get(identity_provider_id=created_by_id)

    if not slug or not name:
        return JsonResponse({"error": "Slug and name are required"}, status=400)

    # Create the organization in the database
    organization = Organization.objects.create(
        name=name,
        slug=slug,
        metadata=metadata if metadata is not None else {},
        identity_provider_id=identity_provider_id,
        created_by=user
    )
    return organization