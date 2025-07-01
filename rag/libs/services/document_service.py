# Document service for handling document upload and indexing
import asyncio
import logging
import os
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

@dataclass
class DocumentUploadRequest:
    """Data class for document upload request parameters"""
    file_ids: List[str] = None
    user_id: str = ""
    settings: Dict[str, Any] = None
    reindex: bool = False


class DocumentService:
    """Service for handling document operations"""

    def __init__(self, app=None):
        """Initialize the document service with an app instance"""
        self._app = app
        logger.info(f"Document service initialized with app instance: {self._app}")

        # Store first index for document uploading
        if hasattr(self._app, 'index_manager') and self._app.index_manager.indices:
            self.file_index = self._app.index_manager.indices[0]  # Use the first index by default
            logger.info(f"Using file index: {self.file_index.name}")

            # Set up UI components to get indexing functions
            selector_ui = self.file_index.get_selector_component_ui()
            if hasattr(selector_ui, 'selector_choices'):
                self.first_selector_choices = selector_ui.selector_choices
            else:
                self.first_selector_choices = []

            # Try to get URL indexing function
            self.first_indexing_url_fn = getattr(selector_ui, 'indexing_url_fn', None)
        else:
            logger.warning("No index found in app, document upload will not work properly")
            self.file_index = None
            self.first_selector_choices = []
            self.first_indexing_url_fn = None

    @staticmethod
    def save_temp_file(file_content, filename) -> str:
        """Save file content to a temporary file and return the path"""
        temp_dir = 'tmp'
        os.makedirs(temp_dir, exist_ok=True)

        # Generate a unique filename if one isn't provided
        if not filename:
            filename = f"{uuid.uuid4()}.tmp"

        file_path = os.path.join(temp_dir, filename)

        with open(file_path, 'wb') as f:
            if hasattr(file_content, 'read'):
                # If it's a file-like object, read it
                f.write(file_content.read())
            else:
                # If it's bytes, write directly
                f.write(file_content)

        return file_path

    async def delete_file(self, file_ids):
        indexing_pipeline = self.file_index.get_indexing_pipeline({}, '')
        indexing_pipeline.delete_file(file_ids)

    async def process_upload_request(self, request: DocumentUploadRequest):
        """Process document upload request and return indexed document IDs"""
        settings = request.settings or {}
        indexing_pipeline = self.file_index.get_indexing_pipeline(settings, request.user_id)

        async def async_wrapper():
            for res in indexing_pipeline.stream(request.file_ids, reindex=request.reindex):
                yield res
                await asyncio.sleep(0)

        # Process files if provided
        file_ids, outputs, debugs = [], [], []
        if request.file_ids:
            async for response in async_wrapper():
                try:
                    if response is None:
                        continue
                    if response.channel == "index":
                        if response.content["status"] == "success":
                            outputs.append(f"\u2705 | {response.content['file_name']}")
                        elif response.content["status"] == "failed":
                            yield 'failed'
                            outputs.append(
                                f"\u274c | {response.content['file_name']}: "
                                f"{response.content['message']}"
                            )
                    elif response.channel == 'info':
                        yield response.content
                    elif response.channel == "debug":
                        debugs.append(response.text)
                except StopIteration as e:
                    # StopIteration.value contains the final result from the stream
                    results, index_errors, docs = e.value
                    file_ids.extend([r for r in results if r])
                    errors = index_errors
                    yield {'file_ids': file_ids}
                except Exception as e:
                    logger.error(f"Error in processing stream: {str(e)}", exc_info=True)
                    yield {'file_ids': file_ids}

        yield {'file_ids': file_ids}
