from functools import wraps

from django.http import JsonResponse
from rest_framework import status

from billing.services import get_subscription
from billing.utils import get_token_usage, get_tokens_used_this_month


def require_tokens(min_tokens=1000):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(*args, **kwargs):
            if hasattr(args[0], 'request'):
                request = args[0].request
            else:
                request = args[0]

            if request.organization is not None and request.organization.metadata is not None:
                configuration = request.organization.metadata
                if 'ignore_token_limit' in configuration and configuration['ignore_token_limit'] == 'yes':
                    return view_func(*args, **kwargs)

            user = getattr(request, 'user', None)
            if not user or not user.is_authenticated:
                return JsonResponse({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

            token_usage = get_token_usage(user)

            if token_usage['remaining'] < min_tokens:
                return JsonResponse({'detail': 'Insufficient tokens.'}, status=status.HTTP_402_PAYMENT_REQUIRED)

            subscription = get_subscription(user)
            is_free_plan = not subscription or not subscription.is_active
            if is_free_plan:
                tokens_used_this_month = get_tokens_used_this_month(user)
                one_million = 1_000_000
                if tokens_used_this_month >= one_million:
                    return JsonResponse({'detail': 'Monthly limit reached.'}, status=status.HTTP_402_PAYMENT_REQUIRED)

            return view_func(*args, **kwargs)

        return _wrapped_view

    return decorator
