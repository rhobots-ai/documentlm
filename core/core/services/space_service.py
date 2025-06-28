from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from accounts.models import User
from core.models import DataSource, Space


def add_data_source_to_space(data_sources: list, space_id: str):
    if len(data_sources) == 0:
        # Handle case where no data sources were found (optional)
        raise ValueError("No valid data sources found.")

    with transaction.atomic():
        try:
            space = Space.objects.get(pk=space_id)
        except ObjectDoesNotExist:
            raise ValueError("Conversation not found or access denied")

        space.data_sources.add(*data_sources)

    return space
