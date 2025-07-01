# Add imports from __init__.py
import asyncio
import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Import BasePage for proper inheritance
from libs.ktem.ktem.utils import get_file_names_regex, get_urls
from libs.ktem.ktem.utils.commands import WEB_SEARCH_COMMAND

# Flow imports
from theflow.settings import settings as flowsettings
from theflow.utils.modules import import_dotted_string

logger = logging.getLogger(__name__)

# Other constants
DEFAULT_SETTING = "(default)"
INFO_PANEL_SCALES = {True: 8, False: 4}

WebSearch = None

@dataclass
class ChatRequest:
    """Data class for chat request parameters"""
    chat_input: Dict[str, Any]
    chat_history: List[List[str]]
    user_id: str
    settings: Dict[str, Any]
    conv_id: Optional[str]
    conv_name: Optional[str]
    first_selector_choices: List[List[str]]


# Initialize reasonings dictionary manually
def initialize_reasonings():
    """Initialize the reasonings dictionary with available reasoning classes"""
    try:
        from libs.ktem.ktem.reasoning.simple import FullQAPipeline, FullDecomposeQAPipeline
        from libs.ktem.ktem.reasoning.react import ReactAgentPipeline
        from libs.ktem.ktem.reasoning.rewoo import RewooAgentPipeline

        # Initialize reasonings dictionary
        reasoning_dict = {
            'simple': FullQAPipeline,
            'complex': FullDecomposeQAPipeline,
            'react': ReactAgentPipeline,
            'rewoo': RewooAgentPipeline
        }

        print(f"Successfully initialized reasonings dictionary with: {list(reasoning_dict.keys())}")
        return reasoning_dict
    except ImportError as e:
        logger.error(f"Error importing reasoning classes: {e}")
        # Fallback to minimal reasoning dictionary
        try:
            from libs.ktem.ktem.reasoning.simple import FullQAPipeline
            print("Imported FullQAPipeline as fallback")
            return {'simple': FullQAPipeline}
        except ImportError as e:
            logger.error(f"Could not import any reasoning classes: {e}")
            return {}


class ChatService:
    """Service class for handling chat operations"""

    def __init__(self, app=None):
        """Initialize the chat service with app instance"""
        self.first_indexing_url_fn = None  # This should be set based on your needs
        self.KH_DEMO_MODE = getattr(flowsettings, "KH_DEMO_MODE", False)
        KH_WEB_SEARCH_BACKEND = getattr(flowsettings, "KH_WEB_SEARCH_BACKEND", None)
        self._use_suggestion = getattr(flowsettings, "KH_FEATURE_CHAT_SUGGESTION", False)
        self.msg_placeholder = getattr(flowsettings, "KH_CHAT_MSG_PLACEHOLDER", "Thinking ...")
        self.empty_msg = getattr(flowsettings, "KH_CHAT_EMPTY_MSG_PLACEHOLDER", "(Sorry, I don't know)")

        # self.KH_DEMO_MODE = False
        # KH_WEB_SEARCH_BACKEND = None
        # self._use_suggestion = False
        # self.msg_placeholder = "Thinking ..."
        # self.empty_msg = "(Sorry, I don't know)"

        self.DEFAULT_QUESTION = (
            "What is the summary of this document?"
            if not self.KH_DEMO_MODE
            else "What is the summary of this paper?"
        )

        self.WebSearch = None
        if KH_WEB_SEARCH_BACKEND:
            try:
                self.WebSearch = import_dotted_string(KH_WEB_SEARCH_BACKEND, safe=False)
            except (ImportError, AttributeError) as e:
                print(f"Error importing {KH_WEB_SEARCH_BACKEND}: {e}")

        # Store the app instance
        self._app = app

        # Initialize indices selectors
        self._indices_input = []

        # Initialize reasonings
        self.reasonings = initialize_reasonings()

    def submit_message(self, request_data: ChatRequest) -> Dict[str, Any]:
        """
        Process a chat message submission
        """
        print("\n" + "=" * 50)
        print("SUBMIT MESSAGE FUNCTION - PARAMETER DETAILS")
        print("=" * 50)

        # Input Parameters Debug
        print("\nINPUT PARAMETERS:")
        print("1. chat_input:")
        print(f"   - Type: {type(request_data.chat_input)}")
        print(f"   - Value: {request_data.chat_input}")

        print("\n2. chat_history:")
        print(f"   - Type: {type(request_data.chat_history)}")
        print(f"   - Length: {len(request_data.chat_history)}")
        print(f"   - Content: {request_data.chat_history}")

        # Input Validation
        if not request_data.chat_input:
            print("[ERROR] Empty chat input detected")
            raise ValueError("Input is empty")

        # Extract chat text
        chat_input_text = request_data.chat_input.get("text", "")

        file_ids = []
        used_command = None

        # File Choices Processing
        first_selector_choices_map = {
            item[0]: item[1] for item in request_data.first_selector_choices
        }

        # File Names Processing using imported function
        file_names, chat_input_text = get_file_names_regex(chat_input_text)

        # Web Search Command Check
        if WEB_SEARCH_COMMAND in file_names:
            used_command = WEB_SEARCH_COMMAND

        # URL Processing using imported function
        urls, chat_input_text = get_urls(chat_input_text)

        # Process URLs using the same approach as __init__.py
        if urls and self.first_indexing_url_fn:
            file_ids = self.first_indexing_url_fn(
                "\n".join(urls),
                True,
                request_data.settings,
                request_data.user_id,
                request=None,
            )

        # File Name Processing
        elif file_names:
            for file_name in file_names:
                file_id = first_selector_choices_map.get(file_name)
                if file_id:
                    file_ids.append(file_id)

        # Update selector choices
        request_data.first_selector_choices.extend(zip(urls, file_ids))

        # Default Question Handling
        if not chat_input_text and file_ids:
            chat_input_text = self.DEFAULT_QUESTION

        if not chat_input_text and not request_data.chat_history:
            chat_input_text = self.DEFAULT_QUESTION

        # Update chat history
        chat_history = request_data.chat_history
        if chat_input_text:
            chat_history = chat_history + [(chat_input_text, None)]
        else:
            if not chat_history:
                raise ValueError("Empty chat")

        # Conversation Management
        new_conv_id = None
        new_conv_name = None
        conv_update = None

        # Prepare response
        response = {
            'chat_input': {},
            'chat_history': chat_history,
            'file_ids': file_ids,
            'used_command': used_command,
            'selector_output': {
                'action': 'select' if file_ids else None,
                'value': file_ids,
                'choices': request_data.first_selector_choices
            }
        }

        print("\n" + "=" * 50)
        print("SUBMIT MESSAGE FUNCTION - COMPLETED")
        print("=" * 50 + "\n")

        return response

    def create_pipeline(
            self,
            settings: dict,
            session_reasoning_type: str,
            session_llm: str,
            session_use_mindmap: bool | str,
            session_use_citation: str,
            session_language: str,
            state: dict,
            command_state: str | None,
            user_id: int,
            *selecteds
    ):
        """Create the pipeline from settings"""

        try:
            reasoning_mode = (
                settings["reasoning.use"]
                if session_reasoning_type in (DEFAULT_SETTING, None)
                else session_reasoning_type
            )

            # Check if reasoning_mode exists in reasonings
            if reasoning_mode not in self.reasonings:
                # Fallback to 'simple' or first available
                if 'simple' in self.reasonings:
                    reasoning_mode = 'simple'
                elif self.reasonings:
                    reasoning_mode = list(self.reasonings.keys())[0]
                else:
                    raise ValueError("No reasoning modes available")

            reasoning_cls = self.reasonings[reasoning_mode]
            reasoning_id = reasoning_cls.get_info()["id"]

            # Continue with the existing code
            settings = deepcopy(settings)
            llm_setting_key = f"reasoning.options.{reasoning_id}.llm"
            if llm_setting_key in settings and session_llm not in (
                    DEFAULT_SETTING,
                    None,
                    "",
            ):
                settings[llm_setting_key] = session_llm

            if session_use_mindmap not in (DEFAULT_SETTING, None):
                settings[f"reasoning.options.{reasoning_id}.create_mindmap"] = session_use_mindmap

            if session_use_citation not in (DEFAULT_SETTING, None):
                settings[f"reasoning.options.{reasoning_id}.highlight_citation"] = session_use_citation

            if session_language not in (DEFAULT_SETTING, None):
                settings["reasoning.lang"] = session_language

            # get retrievers
            retrievers = []

            if command_state == WEB_SEARCH_COMMAND:
                # set retriever for web search
                if not self.WebSearch:
                    raise ValueError("Web search back-end is not available.")

                web_search = self.WebSearch()
                retrievers.append(web_search)
            else:
                for index in self._app.index_manager.indices:
                    # index_selected = []
                    # print('index.selector: ', index.selector)
                    # if isinstance(index.selector, int):
                    #     index_selected = selecteds[index.selector]
                    # if isinstance(index.selector, tuple):
                    #     for i in index.selector:
                    #         index_selected.append(selecteds[i])
                    # print('index_selected: ', index_selected)
                    iretrievers = index.get_retriever_pipelines(
                        settings, user_id, selecteds
                    )
                    retrievers += iretrievers

            # Prepare states
            reasoning_state = {
                "app": deepcopy(state["app"]),
                "pipeline": deepcopy(state.get(reasoning_id, {})),
            }
            pipeline = reasoning_cls.get_pipeline(settings, reasoning_state, retrievers)
            print(f"pipeline: {pipeline}")
            return pipeline, reasoning_state

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            raise ValueError(f"Failed to create pipeline: {str(e)}")

    async def chat_fn(
            self,
            conversation_id,
            chat_history,
            settings,
            reasoning_type,
            llm_type,
            use_mind_map,
            use_citation,
            language,
            chat_state,
            command_state,
            user_id,
            *selecteds
    ):
        """Chat function that processes messages and returns streamed responses"""

        text, evidences, plot = "", [], None
        accumulated_token_usage = None  # Initialize accumulator for token usage
        accumulated_mindmap_json = None  # Initialize accumulator for mindmap JSON
        final_answer_object = None  # To store the generator's return value

        chat_input, chat_output = chat_history[-1]
        chat_history = chat_history[:-1]

        # If chat_output is not empty, assume regeneration mode
        if chat_output:
            chat_state["app"]["regen"] = True

        try:
            # Construct the pipeline
            pipeline, reasoning_state = self.create_pipeline(
                settings,
                reasoning_type,
                llm_type,
                use_mind_map,
                use_citation,
                language,
                chat_state,
                command_state,
                user_id,
                *selecteds
            )

            yield {
                'chat_history': [(chat_input, text or self.msg_placeholder)],
                'evidences': evidences,
                'plot': plot,
                'chat_state': chat_state
            }

            async def async_wrapper():
                for res in pipeline.stream(chat_input, conversation_id, chat_history):
                    yield res
                    await asyncio.sleep(0)

            i = 0
            async for response in async_wrapper():
                try:
                    i += 1

                    # Fix: Import-independent Document type checking
                    is_document = (
                            hasattr(response, 'channel') and
                            hasattr(response, 'content')
                    )

                    # Accumulate metadata first, regardless of whether it's a Document
                    if hasattr(response, 'metadata') and isinstance(response.metadata, dict):
                        # Extract token usage if present and update accumulator
                        current_token_usage = response.metadata.get('token_usage')
                        if current_token_usage:
                            accumulated_token_usage = current_token_usage

                        # Extract mindmap JSON if present and update accumulator
                        current_mindmap_json = response.metadata.get('mindmap_json')
                        if current_mindmap_json:
                            accumulated_mindmap_json = current_mindmap_json

                    if not is_document:
                        continue

                    if response.channel is None:
                        continue

                    if response.channel == "chat" or response.channel == "thinking":
                        if response.content is None:
                            text = ""
                        else:
                            text = response.content

                    if response.channel == "info":
                        if type(response.content) is dict and 'doc' in response.content:
                            doc = response.content['doc']
                            evidences.append({
                                'data_source_id': doc.metadata['file_id'],
                                'page_label': doc.metadata['page_label'],
                                'thumbnail': doc.metadata['image_origin'],
                                'score': doc.metadata['llm_trulens_score'] if 'llm_trulens_score' in doc.metadata else 0.0,
                                'text': doc.content,
                                'marked_text': response.content['override_text'] if 'override_text' in response.content else doc.content,
                                'highlight_text': response.content['highlight_text'] if 'highlight_text' in response.content else doc.content,
                                'has_citations': response.content['has_citations']
                            })
                        else:
                            continue

                    elif response.channel == "plot":
                        plot = response.content

                    chat_state[pipeline.get_info()["id"]] = reasoning_state["pipeline"]

                    # Create response data dictionary, always including the accumulated metadata
                    # Create a flag that indicates if this is likely a final response chunk
                    # (helps frontend know when to expect complete data)
                    is_final_chunk = response.channel == "info" and evidences and (
                            accumulated_token_usage is not None or
                            accumulated_mindmap_json is not None
                    )

                    response_data = {
                        'chat_history': [(chat_input, text or self.msg_placeholder)],
                        'channel': response.channel,
                        'evidences': evidences,
                        'plot': plot,
                        'chat_state': chat_state,
                        'token_usage': accumulated_token_usage,  # Use accumulated value
                        'mindmap': accumulated_mindmap_json,  # Use accumulated value
                        'is_final_chunk': is_final_chunk  # Signal to frontend this is likely a final chunk
                    }

                    # Remove None values for token_usage, mindmap, and is_final_chunk if they haven't been found yet
                    response_data = {k: v for k, v in response_data.items() if v is not None}

                    yield response_data

                except StopIteration as e:
                    final_answer_object = e.value  # Capture the returned object
                    if final_answer_object and hasattr(final_answer_object, 'metadata') and isinstance(final_answer_object.metadata, dict):
                        # Final update for accumulated metadata from the returned object
                        final_token_usage = final_answer_object.metadata.get('token_usage')
                        if final_token_usage:
                            accumulated_token_usage = final_token_usage
                        final_mindmap_json = final_answer_object.metadata.get('mindmap_json')
                        if final_mindmap_json:
                            accumulated_mindmap_json = final_mindmap_json
                    else:
                        logger.warning("Final returned object has no metadata or is not as expected.")
                    break  # Exit the while loop

        except ValueError as e:
            import traceback
            trace = traceback.format_exc()
            print('trace: ', trace)
            # Yield final accumulated state even on error if possible
            final_error_response = {
                'error': str(e),
                'chat_history': [(chat_input, text)],  # Include partial text if any
                'evidences': evidences,
                'plot': plot,
                'chat_state': chat_state,
                'token_usage': accumulated_token_usage,
                'mindmap': accumulated_mindmap_json
            }
            yield {k: v for k, v in final_error_response.items() if v is not None}

        except Exception as e:
            import traceback
            trace = traceback.format_exc()
            print('trace: ', trace)
            # Yield final accumulated state even on error if possible
            final_exception_response = {
                'error': f"Error processing request: {str(e)}",
                'details': trace,
                'chat_history': [(chat_input, text)],
                'evidences': evidences,
                'plot': plot,
                'chat_state': chat_state,
                'token_usage': accumulated_token_usage,
                'mindmap': accumulated_mindmap_json
            }
            yield {k: v for k, v in final_exception_response.items() if v is not None}

        # Final yield outside the loop to ensure the last state is sent
        # Now uses potentially updated accumulated values from the StopIteration block
        logger.info("[FINAL_YIELD_DEBUG] Preparing final_yield_data.")
        logger.info(f"[FINAL_YIELD_DEBUG] Current accumulated_token_usage: {accumulated_token_usage}")
        logger.info(f"[FINAL_YIELD_DEBUG] Current accumulated_mindmap_json is set: {accumulated_mindmap_json is not None}")

        # Handle empty response specifically after the loop
        final_text_to_use = text
        if not text:
            final_text_to_use = self.empty_msg

        final_yield_data = {
            'chat_history': chat_history + [(chat_input, final_text_to_use)],
            'evidences': evidences,
            'plot': plot,
            'chat_state': chat_state,
            'token_usage': accumulated_token_usage,  # Use final accumulated value
            'mindmap': accumulated_mindmap_json  # Use final accumulated value
        }
        yield {k: v for k, v in final_yield_data.items() if v is not None}