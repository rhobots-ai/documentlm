"""Document handling endpoints."""
import json
import traceback

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from libs.services.document_service import DocumentService, DocumentUploadRequest
from ..config import DEFAULT_SETTINGS, logger

# Router without prefix to match Flask's URL patterns exactly
router = APIRouter(tags=["documents"])

@router.post("/documents/delete/")
async def document_delete_view(
        request: Request
):
    request_data = await request.json()
    file_ids = request_data.get('file_ids', False)

    document_service = DocumentService(request.app.state.deepcite)
    await document_service.delete_file(file_ids)
    return JSONResponse(content={'message': 'File deleted.'}, status_code=200)


@router.post("/documents/upload/")
async def document_upload_view(
        request: Request
):
    """Handle document upload requests.
    
    Args:
        request: The HTTP request
        
    Returns:
        Upload result or streaming response
    """
    try:
        document_service = DocumentService(request.app.state.deepcite)

        request_data = await request.json()
        stream_response = request_data.get('stream', False)
        user_id = request_data.get('user_id', '')
        reindex_str = request_data.get('reindex', 'false')
        reindex = reindex_str.lower() == 'true' if isinstance(reindex_str, str) else bool(reindex_str)
        file_ids = request_data.get('file_ids', [])

        # Handle URL upload
        if stream_response:
            return StreamingResponse(
                _handle_streaming_upload(document_service, user_id, reindex, file_ids, True),
                media_type="text/event-stream"
            )
        else:
            result = await _handle_upload(document_service, user_id, reindex, file_ids, True)
            return JSONResponse(content=result, status_code=200)

    except ValueError as e:
        logger.error(f"Value error in document upload: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        logger.error(f"Error in document upload: {str(e)}", exc_info=True)
        return JSONResponse(
            {"error": f"Internal server error: {str(e)}"},
            status_code=500
        )


async def _handle_upload(document_service, user_id, reindex, file_ids, is_url: bool = False):
    """Process multipart file upload request."""
    logger.debug("FastAPI: Starting file upload handler")

    try:
        settings = DEFAULT_SETTINGS

        # Create a request object and process it
        upload_request = DocumentUploadRequest(
            file_ids=file_ids,
            user_id=user_id,
            settings=settings,
            reindex=reindex
        )

        result = await document_service.process_upload_request(upload_request)

        return result
    except Exception as e:
        logger.error(f"FastAPI: Unexpected error in file upload handler: {str(e)}", exc_info=True)
        raise


async def _handle_streaming_upload(document_service, user_id, reindex, file_ids, is_url: bool = False):
    """Handle streaming file upload request."""

    # Send initial heartbeat
    yield "event: heartbeat\ndata: {}\n\n"

    try:
        # Send initial progress update
        progress_data = {
            "status": "processing",
            "stage": "files_received",
            "content": {}
        }
        yield f"event: progress\ndata: {json.dumps(progress_data)}\n\n"

        settings = DEFAULT_SETTINGS

        # Create a request object and process it
        upload_request = DocumentUploadRequest(
            file_ids=file_ids,
            user_id=user_id,
            settings=settings,
            reindex=reindex
        )

        async for doc_response in document_service.process_upload_request(upload_request):
            if doc_response == 'failed':
                raise Exception("Upload failed")
            progress_data = {
                "status": "processing",
                "stage": "indexing",
                "content": doc_response
            }
            yield f"event: progress\ndata: {json.dumps(progress_data)}\n\n"

        # Final completion message with a result
        completion_data = {
            "status": "complete",
            "stage": "finished",
            "content": {}
        }
        yield f"event: complete\ndata: {json.dumps(completion_data)}\n\n"
    except Exception as e:
        logger.error(f"FastAPI Streaming: Unexpected error in file upload handler: {str(e)}", exc_info=True)
        error_data = {
            "status": "error",
            "stage": "finished",
            "content": traceback.format_exc()
        }
        yield f"event: error\ndata: {json.dumps(error_data)}\n\n"
        yield "event: complete\ndata: {\"done\": true}\n\n"