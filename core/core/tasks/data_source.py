import traceback

import requests
import sseclient
from celery import shared_task
from django.contrib.auth import get_user_model
from rest_framework import status

from billing.utils import log_usage
from core.models import DataSource
from core.services import DCService

def _update_log(log, data_sources: list[DataSource]):
    for data_source in data_sources:
        log.input_tokens += data_source.data['tokens']

    log.status = status.HTTP_201_CREATED


@shared_task
def index_data_source(data_source_id: str, user_id: str, path: str, is_platform: bool):
    """
    Process and index a data source file.
    
    Args:
        data_source_id: The ID of the data source to be indexed
        user_id: The ID of the user who initiated the indexing
        path: The API endpoint path for logging
        is_platform: Flag indicating if this is a platform request
    """
    # Status constants to avoid magic strings
    STATUS_PROCESSING = 'processing'
    STATUS_INDEXED = 'indexed'
    STATUS_ERRORED = 'errored'
    
    user = get_user_model().objects.get(id=user_id)
    data_source = DataSource.objects.get(id=data_source_id)
    
    with log_usage(user, path, is_platform) as log:
        try:
            log.request_data = {
                "data_source_id": data_source_id,
                "user_id": user_id
            }

            # Update status and start processing
            data_source.update_status(STATUS_PROCESSING)
            
            # Initialize service and start indexing
            dc_service = DCService()
            async_response = dc_service.create_data_source(
                file_ids=[data_source_id],
                user_id=user_id,
                stream=True
            )
            client = sseclient.SSEClient(async_response)
            
            # Process streaming events
            for event in client.events():
                if event.event == 'error':
                    raise requests.RequestException(event.data)
                if event.event == 'complete':
                    break
                # Additional event processing could be added here
            
            # Update status after successful indexing
            data_source = DataSource.objects.get(id=data_source_id)  # Refresh the object
            data_source.update_status(STATUS_INDEXED)
            
            # Update log information
            if 'tokens' in data_source.data:
                log.input_tokens += data_source.data['tokens']
            response_data = data_source.data
            response_data['url'] = data_source.file.url if data_source.data_type != 'url' else None
            log.response_data = response_data
            log.status = status.HTTP_201_CREATED
            
        except requests.RequestException as e:
            # Handle service-specific errors
            data_source.update_status(STATUS_ERRORED)
            log.status = status.HTTP_503_SERVICE_UNAVAILABLE
            log.error_data = f"Service error: {str(e)}\n{traceback.format_exc()}"
            
        except Exception as e:
            # Handle any other unexpected errors
            data_source.update_status(STATUS_ERRORED)
            log.status = status.HTTP_500_INTERNAL_SERVER_ERROR
            log.error_data = traceback.format_exc()