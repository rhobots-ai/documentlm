"""Chat endpoints for handling chat interactions."""
import copy
import json
import uuid
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse, JSONResponse

from libs.services.chat_service import ChatService, ChatRequest
from ..config import DEFAULT_SETTINGS, logger

# Router without prefix to match Flask's URL patterns exactly
router = APIRouter(tags=["chat"])


@router.post("/chat/")
async def chat_view(request: Request):
    """Handle chat message submission.
    
    Args:
        request: HTTP request
        
    Returns:
        Chat response or streaming response
    """
    generated_conv_name: Optional[str] = None
    try:
        # Process the request data directly, like Flask does
        request_data = await request.json()
        if not request_data:
            return JSONResponse(content={"error": "Invalid request data"}, status_code=400)

        chat_service = ChatService(request.app.state.documentlm)

        # --- Start: Conversation Name Generation ---
        is_first_message = not request_data.get('chat_history', [])
        if is_first_message:
            chat_input = request_data.get('chat_input', {})
            first_user_message = chat_input.get('text', '').strip()
            if first_user_message:
                try:
                    generated_conv_name = f"{first_user_message[:30]}"
                except Exception:
                    generated_conv_name = None
        # --- End: Conversation Name Generation ---

        # Create a ChatRequest object
        chat_request = ChatRequest(
            chat_input=request_data.get('chat_input', {}),
            chat_history=request_data.get('chat_history', []),
            user_id=request_data.get('user_id', ''),
            settings=request_data.get('settings', DEFAULT_SETTINGS),
            conv_name=generated_conv_name or request_data.get('conv_name'),
            conv_id=request_data.get('conv_id'),
            first_selector_choices=request_data.get('first_selector_choices', []),
            is_conversation_flow=request_data.get('is_conversation_flow', False)
        )

        # Submit the chat message
        submit_response = chat_service.submit_message(chat_request)

        # Prefer generated name if it exists, otherwise use name potentially set by submit_message
        final_conv_name = generated_conv_name or submit_response.get('conv_name')

        # Extract document IDs from first_selector_choices if available
        document_ids = []
        if request_data.get('first_selector_choices'):
            document_ids = [item[1] for item in request_data['first_selector_choices'] if len(item) > 1]
            logger.info(f"Extracted document IDs from first_selector_choices: {document_ids}")

            # Log each document ID for deeper debugging
            for idx, doc_id in enumerate(document_ids):
                logger.info(f"Document ID #{idx + 1}: {doc_id}")

        # Extract and prepare parameters for chat processing
        selecteds = request_data.get('selecteds', [])

        # If selecteds isn't provided in the request, but extracted document_ids exist
        if not selecteds and document_ids:
            # Fix: Properly unpack document_ids as separate elements (not nested)
            selecteds = document_ids
            logger.info(f"Modified selecteds list with flattened document_ids: {selecteds}")
        # If still no selecteds but file_ids exist in submit_response
        elif not selecteds and submit_response.get('file_ids'):
            # Fix: Properly unpack file_ids as separate elements (not nested)
            file_ids = submit_response.get('file_ids')
            selecteds = file_ids
            logger.info(f"Modified selecteds list with flattened file_ids: {selecteds}")

        # Set the chat parameters
        chat_params = {
            'reasoning_type': request_data.get('reasoning_type'),
            'llm_type': request_data.get('llm_type', ''),
            'use_mind_map': request_data.get('use_mind_map', True),
            'use_citation': request_data.get('use_citation', 'highlight'),
            'language': request_data.get('language', 'en'),
            'chat_state': request_data.get('chat_state', {'app': {}}),
            'command_state': submit_response.get('used_command'),
            'settings': chat_request.settings,
        }

        # Check if streaming is requested
        stream_response = request_data.get('stream', False)

        if stream_response:
            return StreamingResponse(
                _handle_streaming_chat(
                    chat_service,
                    submit_response,
                    chat_params,
                    selecteds,
                    request_data,
                    final_conv_name
                ),
                media_type="text/event-stream"
            )
        else:
            result = await _handle_non_streaming_chat(
                chat_service, submit_response, chat_params, selecteds, request_data, final_conv_name
            )
            return JSONResponse(content=result, status_code=200)

    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=400)
    except Exception as e:
        logger.error(f"Internal server error: {str(e)}", exc_info=True)
        return JSONResponse(
            {"error": f"Internal server error: {str(e)}"},
            status_code=500
        )


async def _handle_streaming_chat(chat_service, submit_response, chat_params, selecteds, request_data, conv_name):
    """Handle streaming chat response."""

    metadata = {"conversation_name": conv_name}

    # Add heartbeat to keep connection alive
    yield "event: heartbeat\ndata: {}\n\n"

    try:
        # Get the appropriate conversation ID based on the flow mode
        conv_id = submit_response.get('conv_id', '') if request_data.get('is_conversation_flow', False) else ""
        latest_message = None
        # Stream each response chunk as an SSE message
        async for chat_response in chat_service.chat_fn(
                conv_id,
                submit_response['chat_history'],
                chat_params['settings'],
                chat_params['reasoning_type'],
                chat_params['llm_type'],
                chat_params['use_mind_map'],
                chat_params['use_citation'],
                chat_params['language'],
                chat_params['chat_state'],
                chat_params['command_state'],
                request_data.get('user_id', ''),
                *selecteds
        ):
            # Process chat response (same as before)
            chat_response['chunk_id'] = str(uuid.uuid4())
            latest_message = copy.deepcopy(chat_response)

            if 'evidences' in chat_response:
                chat_response.pop('evidences')

            # Format as server-sent event
            if 'mindmap' in chat_response:
                chat_response.pop('mindmap')
            if 'token_usage' not in chat_response:
                event = 'thinking' if 'channel' in chat_response and chat_response['channel'] == 'thinking' else 'message'
                yield f"event: {event}\ndata: {json.dumps(chat_response)}\n\n"

        # Process metadata if needed
        if hasattr(latest_message, 'metadata') and latest_message.metadata:
            needs_conversion = False

            # Create a new dictionary if we need to modify the response
            response_dict = {}

            # Check if token_usage is in metadata but not in top-level
            if 'token_usage' not in latest_message and 'token_usage' in latest_message.metadata:
                needs_conversion = True

            # Check if mindmap_json is in metadata
            if 'mindmap_json' in latest_message.metadata:
                needs_conversion = True

            # If we need to convert, do it all at once
            if needs_conversion:
                # Copy all existing top-level attributes
                for key, value in latest_message.items():
                    response_dict[key] = value

                # Add token_usage from metadata if available
                if 'token_usage' in latest_message.metadata:
                    response_dict['token_usage'] = latest_message.metadata['token_usage']

                # Add mindmap from metadata if available
                if 'mindmap_json' in latest_message.metadata:
                    response_dict['mindmap'] = latest_message.metadata['mindmap_json']

                latest_message = response_dict

        # <<< REVISED LOGGING >>>
        stream_token_usage_present = 'token_usage' in latest_message and latest_message['token_usage'] is not None
        stream_mindmap_present = 'mindmap' in latest_message and latest_message['mindmap'] is not None
        logger.info(
            f"Streaming chunk about to be sent. Chunk ID: {latest_message.get('chunk_id', 'N/A')}. Keys: {list(latest_message.keys())}. Has token_usage: {stream_token_usage_present}. Has mindmap: {stream_mindmap_present}.")
        # <<< END REVISED LOGGING >>>

        yield f"event: message\ndata: {json.dumps(latest_message)}\n\n"

        # Signal end of stream
        yield "event: complete\ndata: {\"done\": True}\n\n"
        yield "stop"
    except Exception as e:
        logger.error(f"Error in streaming response: {str(e)}", exc_info=True)
        yield f"event: error\ndata: {json.dumps({'error': str(e), 'chat_history': submit_response['chat_history']})}\n\n"
        yield "event: complete\ndata: {\"done\": True}\n\n"


async def _handle_non_streaming_chat(chat_service, submit_response, chat_params, selecteds, request_data, conv_name):
    # Collect chat responses
    responses = []
    # Get the appropriate conversation ID based on the flow mode
    conv_id = submit_response.get('conv_id', '') if request_data.get('is_conversation_flow', False) else ""

    answer = ''
    async for response in chat_service.chat_fn(
            conv_id,  # Use conversation ID based on flow mode
            submit_response['chat_history'],
            chat_params['settings'],
            chat_params['reasoning_type'],
            chat_params['llm_type'],
            chat_params['use_mind_map'],
            chat_params['use_citation'],
            chat_params['language'],
            chat_params['chat_state'],
            chat_params['command_state'],
            request_data.get('user_id', ''),
            *selecteds
    ):
        answer_chunk = response['chat_history'][-1][-1]
        if answer_chunk != 'Thinking ...':
            answer += answer_chunk
        responses.append(response)

    if responses:
        last_response = responses[-1]

        # Get the last chat history entry (as a list)
        last_entry = list(last_response['chat_history'][-1])
        # Modify the last element
        last_entry[-1] = answer
        # Update the chat history
        last_response['chat_history'][-1] = tuple(last_entry)

        # <<< ADDED LOGGING >>>
        logger.info(f"Non-streaming: Last response received from chat_fn. Type: {type(last_response)}")
        if isinstance(last_response, dict):
            logger.info(f"Non-streaming: Last response is dict. Keys: {list(last_response.keys())}")
            final_response_content = last_response  # Use the last dict as the base
        elif hasattr(last_response, 'metadata') and isinstance(last_response.metadata, dict):
            logger.info(f"Non-streaming: Last response is Document. Metadata keys: {list(last_response.metadata.keys())}")
            # Reconstruct response dict if last item was a Document (shouldn't happen with new service logic)
            final_response_content = {
                'chat_history': submit_response['chat_history'],  # Use history from submit
                'plot': None,  # Default plot
                'chat_state': chat_params['chat_state'],  # Use chat_state from params
                'token_usage': last_response.metadata.get('token_usage'),
                'mindmap': last_response.metadata.get('mindmap_json')
            }
        else:
            logger.warning("Non-streaming: Last response is neither a dict nor a Document with metadata.")
            # Fallback if last response is unexpected type
            final_response_content = {
                'chat_history': submit_response['chat_history'],
                'plot': None,
                'chat_state': chat_params['chat_state'],
            }
    # <<< END ADDED LOGGING >>>
    else:
        logger.warning("Non-streaming: No responses received from chat_fn.")
        # Fallback if no responses were generated
        final_response_content = {
            'chat_history': submit_response['chat_history'],
            'plot': None,
            'chat_state': chat_params['chat_state'],
        }

    # Combine submit_response fields with final content, ensuring final content takes precedence for overlapping keys like chat_history
    result = {**submit_response, **final_response_content}

    # Explicitly check for data again in the final combined dict
    final_token_usage_present = 'token_usage' in result and result['token_usage'] is not None
    final_mindmap_present = 'mindmap' in result and result['mindmap'] is not None

    # Always include document_ref in the result, even if empty
    # This ensures the frontend always sees the document_ref key
    result['document_ref'] = []
    result['conversation_name'] = conv_name

    # Log final state before sending
    logger.info(
        f"Final non-streaming response about to be sent. Keys: {list(result.keys())}. Has token_usage: {final_token_usage_present}. Has mindmap: {final_mindmap_present}.")
    if final_token_usage_present:
        logger.info(f"Final token_usage totals: {result['token_usage'].get('totals', 'N/A')}")
    if final_mindmap_present:
        logger.info(f"Final mindmap data type: {type(result['mindmap'])}")

    return result
