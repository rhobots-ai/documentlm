import json
import logging
import threading
from datetime import datetime
from textwrap import dedent
from typing import Generator

import tiktoken
from decouple import config
from libs.ktem.ktem.embeddings.manager import embedding_models_manager as embeddings
from libs.ktem.ktem.llms.manager import llms
from libs.ktem.ktem.reasoning.prompt_optimization import (
    DecomposeQuestionPipeline,
    RewriteQuestionPipeline,
)
from libs.ktem.ktem.utils.render import Render
from libs.ktem.ktem.utils.visualize_cited import CreateCitationVizPipeline
from plotly.io import to_json

from libs.kotaemon.kotaemon.base import (
    AIMessage,
    BaseComponent,
    Document,
    HumanMessage,
    Node,
    RetrievedDocument,
    SystemMessage,
)
from libs.kotaemon.kotaemon.indices.qa.citation_qa import (
    CONTEXT_RELEVANT_WARNING_SCORE,
    DEFAULT_QA_TEXT_PROMPT,
    AnswerWithContextPipeline
)
from libs.kotaemon.kotaemon.indices.qa.citation_qa_inline import AnswerWithInlineCitation
from libs.kotaemon.kotaemon.indices.qa.format_context import PrepareEvidencePipeline
from libs.kotaemon.kotaemon.indices.qa.utils import replace_think_tag_with_details
from libs.kotaemon.kotaemon.llms import ChatLLM

from ..utils import SUPPORTED_LANGUAGE_MAP
from .base import BaseReasoning

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class AddQueryContextPipeline(BaseComponent):
    n_last_interactions: int = 5
    llm: ChatLLM = Node(default_callback=lambda _: llms.get_default())

    def run(self, question: str, history: list) -> Document:
        messages = [
            SystemMessage(
                content="Below is a history of the conversation so far, and a new "
                        "question asked by the user that needs to be answered by searching "
                        "in a knowledge base.\nYou have access to a Search index "
                        "with 100's of documents.\nGenerate a search query based on the "
                        "conversation and the new question.\nDo not include cited source "
                        "filenames and document names e.g info.txt or doc.pdf in the search "
                        "query terms.\nDo not include any text inside [] or <<>> in the "
                        "search query terms.\nDo not include any special characters like "
                        "'+'.\nIf the question is not in English, rewrite the query in "
                        "the language used in the question.\n If the question contains enough "
                        "information, return just the number 1\n If it's unnecessary to do "
                        "the searching, return just the number 0."
            ),
            HumanMessage(content="How did crypto do last year?"),
            AIMessage(
                content="Summarize Cryptocurrency Market Dynamics from last year"
            ),
            HumanMessage(content="What are my health plans?"),
            AIMessage(content="Show available health plans"),
        ]
        for human, ai in history[-self.n_last_interactions:]:
            messages.append(HumanMessage(content=human))
            messages.append(AIMessage(content=ai))

        messages.append(HumanMessage(content=f"Generate search query for: {question}"))

        resp = self.llm(messages).text
        if resp == "0":
            return Document(content="")

        if resp == "1":
            return Document(content=question)

        return Document(content=resp)


class FullQAPipeline(BaseReasoning):
    """Question answering pipeline. Handle from question to answer"""

    class Config:
        allow_extra = True

    # configuration parameters
    trigger_context: int = 150
    use_rewrite: bool = False

    retrievers: list[BaseComponent]

    evidence_pipeline: PrepareEvidencePipeline = PrepareEvidencePipeline.withx()
    answering_pipeline: AnswerWithContextPipeline
    rewrite_pipeline: RewriteQuestionPipeline | None = None
    create_citation_viz_pipeline: CreateCitationVizPipeline = Node(
        default_callback=lambda _: CreateCitationVizPipeline(
            embedding=embeddings.get_default()
        )
    )
    add_query_context: AddQueryContextPipeline = AddQueryContextPipeline.withx()

    def get_token_counter(self, model_name: str = None):
        """Get a tokenizer for the specified model"""
        try:
            if not model_name or model_name == "default":
                # Default to gpt-3.5-turbo if no model specified
                return tiktoken.encoding_for_model("gpt-3.5-turbo")

            # For OpenAI models
            if model_name.startswith(("gpt-", "text-embedding-")):
                return tiktoken.encoding_for_model(model_name)

            # For Google models
            if model_name.startswith("gemini-"):
                return tiktoken.encoding_for_model("cl100k_base")

            # For Anthropic models
            if model_name.startswith("claude-"):
                return tiktoken.encoding_for_model("cl100k_base")

            # For Cohere models
            if model_name.startswith("command-"):
                return tiktoken.encoding_for_model("cl100k_base")

            # Fallback to cl100k_base for other models
            return tiktoken.encoding_for_model("cl100k_base")
        except Exception as e:
            logger.warning(f"Error creating tokenizer for {model_name}: {e}")
            # Fallback to cl100k_base if specific model encoding not available
            return tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str, model_name: str = None) -> int:
        """Count tokens in a string using tiktoken"""
        if not text:
            return 0

        tokenizer = self.get_token_counter(model_name)
        return len(tokenizer.encode(str(text)))

    def count_message_tokens(self, messages: list, model_name: str = None) -> dict:
        """Count tokens in a message list (for chat models)"""
        if not messages:
            return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        tokenizer = self.get_token_counter(model_name)
        prompt_tokens = 0

        for message in messages:
            # Common tokens per message (3 for 'role': 'content': and message separator)
            prompt_tokens += 3

            # Count content tokens
            if hasattr(message, "content"):
                content = message.content
                if isinstance(content, str):
                    prompt_tokens += len(tokenizer.encode(content))
                elif isinstance(content, list):
                    # Handle multimodal content (text + images)
                    for item in content:
                        if isinstance(item, dict) and item.get("type") == "text":
                            prompt_tokens += len(tokenizer.encode(item.get("text", "")))
                        # For images, approximate token count based on OpenAI's guidance
                        elif isinstance(item, dict) and item.get("type") == "image_url":
                            # Approximate image tokens (1000 per image as a default)
                            prompt_tokens += 1000

            # Count additional fields if present
            for field in ["name", "function_call"]:
                if hasattr(message, field) and getattr(message, field):
                    prompt_tokens += len(tokenizer.encode(str(getattr(message, field))))
                    prompt_tokens += 1  # +1 for the field overhead

        # Add per-request overhead (OpenAI specific, but good approximation)
        prompt_tokens += 3

        return {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": 0,  # Will be populated after completion
            "total_tokens": prompt_tokens
        }

    def init_token_usage_data(self, model_name: str, conv_id: str):
        """Initialize token usage tracking structure"""
        return {
            "model": model_name,
            "timestamp": datetime.now().isoformat(),
            "conversation_id": conv_id,
            "components": {
                "rewrite_pipeline": {
                    "used": False,
                    "tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0
                },
                "add_query_context": {
                    "used": False,
                    "tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0
                },
                "retrieve": {
                    "tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0
                },
                "evidence_pipeline": {
                    "tokens": 0
                },
                "answering_pipeline": {
                    "tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0
                },
                "citation_pipeline": {
                    "used": False,
                    "tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0
                },
                "mindmap_pipeline": {
                    "used": False,
                    "tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0
                },
                "citation_viz": {
                    "used": False,
                    "tokens": 0
                }
            },
            "totals": {
                "tokens": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "cost": 0.0
            }
        }

    def retrieve(
            self, message: str, history: list, token_usage=None
    ) -> tuple[list[RetrievedDocument], list[Document]]:
        """Retrieve the documents based on the message"""
        # Initialize model_name for token counting
        model_name = getattr(self.answering_pipeline.llm, "model", "default") if hasattr(self, "answering_pipeline") else "default"

        # Store original message tokens for potential add_query_context usage
        original_message_tokens = self.count_tokens(message, model_name) if token_usage else 0

        # This section is commented out but we're preparing token tracking for when it's enabled
        if len(message) < self.trigger_context and token_usage:
            # prefer adding context for short user questions, avoid adding context for
            # long questions, as they are likely to contain enough information
            # plus, avoid the situation where the original message is already too long
            # for the model to handle

            # Track token usage before calling add_query_context
            token_usage["components"]["add_query_context"]["used"] = True
            token_usage["components"]["add_query_context"]["prompt_tokens"] = original_message_tokens

            # Uncomment the next lines when ready to enable add_query_context
            # query_doc = self.add_query_context(message, history)
            # query = query_doc.content
            # rewritten_query_tokens = self.count_tokens(query, model_name)
            # token_usage["components"]["add_query_context"]["completion_tokens"] = rewritten_query_tokens
            # token_usage["components"]["add_query_context"]["tokens"] = original_message_tokens + rewritten_query_tokens
            # print(f"Rewritten query: {query}")
        else:
            query = message

        query = None
        if not query:
            # TODO: previously return [], [] because we think this message as something
            # like "Hello", "I need help"...
            query = message

        docs, doc_ids = [], []
        plot_docs = []

        for idx, retriever in enumerate(self.retrievers):
            retriever_node = self._prepare_child(retriever, f"retriever_{idx}")
            retriever_docs = retriever_node(text=query)

            retriever_docs_text = []
            retriever_docs_plot = []

            for doc in retriever_docs:
                if doc.metadata.get("type", "") == "plot":
                    retriever_docs_plot.append(doc)
                else:
                    retriever_docs_text.append(doc)

            for doc in retriever_docs_text:
                if doc.doc_id not in doc_ids:
                    docs.append(doc)
                    doc_ids.append(doc.doc_id)

            plot_docs.extend(retriever_docs_plot)

        info = [
                Document(
                    channel="info",
                    content=Render.collapsible_with_header(doc, open_collapsible=True),
                )
                for doc in docs
            ] + [
                Document(
                    channel="plot",
                    content=doc.metadata.get("data", ""),
                )
                for doc in plot_docs
            ]

        return docs, info

    def prepare_mindmap(self, answer) -> Document | None:
        mindmap = answer.metadata["mindmap"]
        if mindmap:
            mindmap_text = mindmap.text

            # Get the JSON structure from mindmap's metadata
            mindmap_json = mindmap.metadata.get("json_structure", {})

            mindmap_svg = dedent(
                """
                <div class="markmap">
                <script type="text/template">
                ---
                markmap:
                    colorFreezeLevel: 2
                    activeNode:
                        placement: center
                    initialExpandLevel: 4
                    maxWidth: 200
                ---
                {}
                </script>
                </div>
                """
            ).format(mindmap_text)

            mindmap_content = Document(
                channel="info",
                content=Render.collapsible(
                    header="""
                    <i>Mindmap</i>
                    <a href="#" id='mindmap-toggle'>
                        [Expand]</a>
                    <a href="#" id='mindmap-export'>
                        [Export]</a>""",
                    content=mindmap_svg,
                    open=True,
                ),
                metadata={"mindmap_json": mindmap_json}  # Add JSON to metadata
            )
        else:
            mindmap_content = None

        return mindmap_content

    def prepare_citation_viz(self, answer, question, docs) -> Document | None:
        doc_texts = [doc.text for doc in docs]
        citation_plot = None
        plot_content = None

        if answer.metadata["citation_viz"] and len(docs) > 1:
            try:
                citation_plot = self.create_citation_viz_pipeline(doc_texts, question)
            except Exception as e:
                print("Failed to create citation plot:", e)

            if citation_plot:
                plot = to_json(citation_plot)
                plot_content = Document(channel="plot", content=plot)

        return plot_content

    def show_citations_and_addons(self, answer, docs, question):
        # show the evidence
        with_citation, without_citation, raw_with_citation, raw_without_citation = self.answering_pipeline.prepare_citations(
            answer, docs
        )

        # Add extra debug logging for inline citations
        if isinstance(self.answering_pipeline, AnswerWithInlineCitation):
            try:
                logger.info("Using inline citation pipeline, checking documentation references and links")
                # Call debug logging method if available
                if hasattr(self.answering_pipeline, "log_citation_info"):
                    self.answering_pipeline.log_citation_info(answer, docs, with_citation)
            except Exception as e:
                logger.error(f"Error during inline citation debugging: {str(e)}")

        mindmap_output = self.prepare_mindmap(answer)
        citation_plot_output = self.prepare_citation_viz(answer, question, docs)

        if not with_citation and not without_citation:
            logger.warning("No citation documents were generated by the answering pipeline")
            yield Document(channel="info", content="<h5><b>No evidence found.</b></h5>")
        else:
            logger.info(f"Generated {len(with_citation)} citation documents and {len(without_citation)} non-citation documents")
            # clear the Info panel
            max_llm_rerank_score = max(
                doc.metadata.get("llm_trulens_score", 0.0) for doc in docs
            )
            has_llm_score = any("llm_trulens_score" in doc.metadata for doc in docs)
            # clear previous info
            yield Document(channel="info", content=None)

            # yield mindmap output
            if mindmap_output:
                yield mindmap_output

            # yield citation plot output
            if citation_plot_output:
                yield citation_plot_output

            # Correctly yield token_usage Document if present
            if 'token_usage' in answer.metadata:
                yield Document(
                    channel="info",  # Changed from "metadata" to valid channel
                    content=None,
                    metadata={'token_usage': answer.metadata['token_usage']}
                )

            # Correctly indented warning message
            if has_llm_score and max_llm_rerank_score < CONTEXT_RELEVANT_WARNING_SCORE:
                yield Document(
                    channel="info",
                    content=(
                        "<h5>WARNING! Context relevance score is low. "
                        "Double check the model answer for correctness.</h5>"
                    ),
                )

            # show QA score
            qa_score = (
                round(answer.metadata["qa_score"], 2)
                if answer.metadata.get("qa_score")
                else None
            )
            if qa_score:
                yield Document(
                    channel="info",
                    content=f"<h5>Answer confidence: {qa_score}</h5>",
                )

            yield from with_citation
            if without_citation:
                yield from without_citation

            yield from raw_with_citation
            if raw_without_citation:
                yield from raw_without_citation

    async def ainvoke(  # type: ignore
            self, message: str, conv_id: str, history: list, **kwargs  # type: ignore
    ) -> Document:  # type: ignore
        raise NotImplementedError

    def stream(  # type: ignore
            self, message: str, conv_id: str = "", history: list = None, **kwargs  # type: ignore
    ) -> Generator[Document, None, Document]:
        # Make history default to empty list if None
        history = history or []

        # Initialize token usage tracking
        model_name = getattr(self.answering_pipeline.llm, "model", "default")
        token_usage = self.init_token_usage_data(model_name, conv_id)

        # Note: conv_id is kept for backward compatibility but is not used for critical functionality
        if self.use_rewrite and self.rewrite_pipeline:
            question_tokens = self.count_tokens(message, model_name)
            message = self.rewrite_pipeline(question=message).text
            rewrite_result_tokens = self.count_tokens(message, model_name)

            # Track rewrite pipeline token usage
            token_usage["components"]["rewrite_pipeline"]["used"] = True
            token_usage["components"]["rewrite_pipeline"]["prompt_tokens"] = question_tokens
            token_usage["components"]["rewrite_pipeline"]["completion_tokens"] = rewrite_result_tokens
            token_usage["components"]["rewrite_pipeline"]["tokens"] = question_tokens + rewrite_result_tokens


        # should populate the context
        docs, infos = self.retrieve(message, history)

        # Count tokens in retrieved documents
        doc_tokens = sum(self.count_tokens(doc.text, model_name) for doc in docs)
        token_usage["components"]["retrieve"]["tokens"] = doc_tokens

        yield from infos

        evidence_mode, evidence, images = self.evidence_pipeline(docs).content

        # Count tokens in evidence
        evidence_tokens = self.count_tokens(evidence, model_name)
        token_usage["components"]["evidence_pipeline"]["tokens"] = evidence_tokens

        def generate_relevant_scores():
            nonlocal docs
            docs = self.retrievers[0].generate_relevant_scores(message, docs)

        # generate relevant score using
        if evidence and self.retrievers:
            scoring_thread = threading.Thread(target=generate_relevant_scores)
            scoring_thread.start()
        else:
            scoring_thread = None

        # Count tokens for answering pipeline
        messages = []
        if hasattr(self.answering_pipeline, "system_prompt") and self.answering_pipeline.system_prompt:
            system_prompt_tokens = self.count_tokens(self.answering_pipeline.system_prompt, model_name)
            token_usage["components"]["answering_pipeline"]["prompt_tokens"] += system_prompt_tokens

        # Count history tokens
        if history:
            history_tokens = sum(self.count_tokens(h, model_name) + self.count_tokens(a, model_name)
                              for h, a in history[-self.answering_pipeline.n_last_interactions:])
            token_usage["components"]["answering_pipeline"]["prompt_tokens"] += history_tokens

        # Count question and evidence tokens
        question_tokens = self.count_tokens(message, model_name)
        token_usage["components"]["answering_pipeline"]["prompt_tokens"] += question_tokens + evidence_tokens

        answer = yield from self.answering_pipeline.stream(
            question=message,
            history=history,
            evidence=evidence,
            evidence_mode=evidence_mode,
            images=images,
            conv_id=conv_id,
            **kwargs,
        )

        # Count completion tokens
        completion_tokens = self.count_tokens(answer.text, model_name)
        token_usage["components"]["answering_pipeline"]["completion_tokens"] = completion_tokens
        token_usage["components"]["answering_pipeline"]["tokens"] = token_usage["components"]["answering_pipeline"]["prompt_tokens"] + completion_tokens

        # Check if mindmap was generated
        if answer.metadata.get("mindmap"):
            token_usage["components"]["mindmap_pipeline"]["used"] = True
            # Track input tokens (question + evidence)
            mindmap_input_tokens = self.count_tokens(message, model_name) + evidence_tokens
            # Track output tokens (mindmap text)
            mindmap_output_tokens = self.count_tokens(answer.metadata["mindmap"].text, model_name)
            token_usage["components"]["mindmap_pipeline"]["prompt_tokens"] = mindmap_input_tokens
            token_usage["components"]["mindmap_pipeline"]["completion_tokens"] = mindmap_output_tokens
            token_usage["components"]["mindmap_pipeline"]["tokens"] = mindmap_input_tokens + mindmap_output_tokens

            # Extract the JSON structure from mindmap's metadata and add it directly to answer metadata
            # This ensures the mindmap JSON is in the same Document as token_usage
            if answer.metadata["mindmap"].metadata and "json_structure" in answer.metadata["mindmap"].metadata:
                answer.metadata["mindmap_json"] = answer.metadata["mindmap"].metadata["json_structure"]
                print("Added mindmap_json directly to answer metadata")

        # Check if citation was generated
        if answer.metadata.get("citation"):
            token_usage["components"]["citation_pipeline"]["used"] = True
            # Track input tokens (question + evidence)
            citation_input_tokens = self.count_tokens(message, model_name) + evidence_tokens
            # Track output tokens (evidences)
            citation_output_tokens = 0

            # Handle different citation data structures (highlight vs inline)
            if hasattr(answer.metadata["citation"], "evidences"):
                # For highlight citation
                citation_output_tokens = sum(self.count_tokens(e, model_name)
                                       for e in answer.metadata["citation"].evidences)
            else:
                # For inline citation (list structure)
                logger.info("Detected inline citation format (list) for token counting")
                try:
                    citation_output_tokens = sum(self.count_tokens(str(e), model_name)
                                           for e in answer.metadata["citation"])
                except Exception as e:
                    logger.error(f"Error counting inline citation tokens: {str(e)}")
                    # Default to a reasonable estimate
                    citation_output_tokens = len(answer.metadata["citation"]) * 50

            token_usage["components"]["citation_pipeline"]["prompt_tokens"] = citation_input_tokens
            token_usage["components"]["citation_pipeline"]["completion_tokens"] = citation_output_tokens
            token_usage["components"]["citation_pipeline"]["tokens"] = citation_input_tokens + citation_output_tokens

        # Check if citation viz was generated
        if answer.metadata.get("citation_viz"):
            token_usage["components"]["citation_viz"]["used"] = True
            # Approximation as embeddings are used
            token_usage["components"]["citation_viz"]["tokens"] = len(docs) * 1000  # Rough estimate

        # Calculate totals including all LLM calls
        token_usage["totals"]["prompt_tokens"] = (
            token_usage["components"]["answering_pipeline"]["prompt_tokens"] +
            (token_usage["components"]["rewrite_pipeline"]["prompt_tokens"] if token_usage["components"]["rewrite_pipeline"]["used"] else 0) +
            (token_usage["components"]["citation_pipeline"]["prompt_tokens"] if token_usage["components"]["citation_pipeline"]["used"] else 0) +
            (token_usage["components"]["mindmap_pipeline"]["prompt_tokens"] if token_usage["components"]["mindmap_pipeline"]["used"] else 0) +
            (token_usage["components"]["add_query_context"]["prompt_tokens"] if token_usage["components"]["add_query_context"]["used"] else 0)
        )
        token_usage["totals"]["completion_tokens"] = (
            token_usage["components"]["answering_pipeline"]["completion_tokens"] +
            (token_usage["components"]["rewrite_pipeline"]["completion_tokens"] if token_usage["components"]["rewrite_pipeline"]["used"] else 0) +
            (token_usage["components"]["citation_pipeline"]["completion_tokens"] if token_usage["components"]["citation_pipeline"]["used"] else 0) +
            (token_usage["components"]["mindmap_pipeline"]["completion_tokens"] if token_usage["components"]["mindmap_pipeline"]["used"] else 0) +
            (token_usage["components"]["add_query_context"]["completion_tokens"] if token_usage["components"]["add_query_context"]["used"] else 0)
        )
        token_usage["totals"]["tokens"] = token_usage["totals"]["prompt_tokens"] + token_usage["totals"]["completion_tokens"]

        # Save token usage to answer metadata and print debug info
        logger.debug(f"Final calculated token_usage before attaching to metadata:\n{json.dumps(token_usage, indent=2)}")
        answer.metadata["token_usage"] = token_usage

        # check <think> tag from reasoning models
        processed_answer = replace_think_tag_with_details(answer.text)
        if processed_answer != answer.text:
            # clear the chat message and render again
            yield Document(channel="chat", content=None)
            yield Document(channel="chat", content=processed_answer)

        # show the evidence
        if scoring_thread:
            scoring_thread.join()

        yield from self.show_citations_and_addons(answer, docs, message)

        return answer

    @classmethod
    def prepare_pipeline_instance(cls, settings, retrievers):
        return cls(
            retrievers=retrievers,
            rewrite_pipeline=None,
        )

    @classmethod
    def get_pipeline(cls, settings, states, retrievers):
        """Get the reasoning pipeline

        Args:
            settings: the settings for the pipeline
            retrievers: the retrievers to use
        """
        max_context_length_setting = settings.get("reasoning.max_context_length", 32000)

        pipeline = cls.prepare_pipeline_instance(settings, retrievers)

        prefix = f"reasoning.options.{cls.get_info()['id']}"
        llm_name = settings.get(f"{prefix}.llm", None)
        llm = llms.get(llm_name, llms.get_default())

        # prepare evidence pipeline configuration
        evidence_pipeline = pipeline.evidence_pipeline
        evidence_pipeline.max_context_length = max_context_length_setting

        # answering pipeline configuration
        # First check for direct citation style
        if hasattr(settings, "get") and callable(settings.get):
            # Try to get the direct use_citation parameter
            citation_style = settings.get('use_citation')
            if citation_style is None:  # If not found directly
                # Fall back to the old nested path
                citation_style = settings.get(f"{prefix}.highlight_citation", "highlight")
        else:
            # Handle the case where settings might not be a dictionary
            citation_style = "highlight"  # Default

        # Determine if inline citation should be used
        use_inline_citation = citation_style == "inline"

        # Log citation style selection for debugging
        logger.info(f"Citation style selected: '{citation_style}' (use_inline_citation={use_inline_citation})")
        if use_inline_citation:
            answer_pipeline = pipeline.answering_pipeline = AnswerWithInlineCitation()
            logger.info(f"Using inline citation style (from setting: {citation_style})")
        else:
            answer_pipeline = pipeline.answering_pipeline = AnswerWithContextPipeline()
            logger.info(f"Using highlight citation style (from setting: {citation_style})")

        answer_pipeline.llm = llm
        answer_pipeline.citation_pipeline.llm = llm
        answer_pipeline.n_last_interactions = settings[f"{prefix}.n_last_interactions"]
        answer_pipeline.enable_citation = (
                settings[f"{prefix}.highlight_citation"] != "off"
        )
        answer_pipeline.enable_mindmap = settings[f"{prefix}.create_mindmap"]
        answer_pipeline.enable_citation_viz = settings[f"{prefix}.create_citation_viz"]
        answer_pipeline.use_multimodal = settings[f"{prefix}.use_multimodal"]
        answer_pipeline.system_prompt = settings[f"{prefix}.system_prompt"]
        answer_pipeline.qa_template = settings[f"{prefix}.qa_prompt"]
        answer_pipeline.lang = SUPPORTED_LANGUAGE_MAP.get(
            settings["reasoning.lang"], "English"
        )

        pipeline.add_query_context.llm = llm
        pipeline.add_query_context.n_last_interactions = settings[
            f"{prefix}.n_last_interactions"
        ]

        pipeline.trigger_context = settings[f"{prefix}.trigger_context"]
        pipeline.use_rewrite = states.get("app", {}).get("regen", False)
        if pipeline.rewrite_pipeline:
            pipeline.rewrite_pipeline.llm = llm
            pipeline.rewrite_pipeline.lang = SUPPORTED_LANGUAGE_MAP.get(
                settings["reasoning.lang"], "English"
            )
        return pipeline

    @classmethod
    def get_user_settings(cls) -> dict:
        from libs.ktem.ktem.llms.manager import llms

        llm = ""
        choices = [("(default)", "")]
        try:
            choices += [(_, _) for _ in llms.options().keys()]
        except Exception as e:
            logger.exception(f"Failed to get LLM options: {e}")

        return {
            "llm": {
                "name": "Language model",
                "value": llm,
                "component": "dropdown",
                "choices": choices,
                "special_type": "llm",
                "info": (
                    "The language model to use for generating the answer. If None, "
                    "the application default language model will be used."
                ),
            },
            "highlight_citation": {
                "name": "Citation style",
                "value": (
                    "highlight"
                    if not config("USE_LOW_LLM_REQUESTS", default=False, cast=bool)
                    else "off"
                ),
                "component": "radio",
                "choices": [
                    ("citation: highlight", "highlight"),
                    ("citation: inline", "inline"),
                    ("no citation", "off"),
                ],
            },
            "create_mindmap": {
                "name": "Create Mindmap",
                "value": False,
                "component": "checkbox",
            },
            "create_citation_viz": {
                "name": "Create Embeddings Visualization",
                "value": False,
                "component": "checkbox",
            },
            "use_multimodal": {
                "name": "Use Multimodal Input",
                "value": False,
                "component": "checkbox",
            },
            "system_prompt": {
                "name": "System Prompt",
                "value": ("This is a question answering system."),
            },
            "qa_prompt": {
                "name": "QA Prompt (contains {context}, {question}, {lang})",
                "value": DEFAULT_QA_TEXT_PROMPT,
            },
            "n_last_interactions": {
                "name": "Number of interactions to include",
                "value": 5,
                "component": "number",
                "info": "The maximum number of chat interactions to include in the LLM",
            },
            "trigger_context": {
                "name": "Maximum message length for context rewriting",
                "value": 150,
                "component": "number",
                "info": (
                    "The maximum length of the message to trigger context addition. "
                    "Exceeding this length, the message will be used as is."
                ),
            },
        }

    @classmethod
    def get_info(cls) -> dict:
        return {
            "id": "simple",
            "name": "Simple QA",
            "description": (
                "Simple RAG-based question answering pipeline. This pipeline can "
                "perform both keyword search and similarity search to retrieve the "
                "context. After that it includes that context to generate the answer."
            ),
        }


class FullDecomposeQAPipeline(FullQAPipeline):
    def answer_sub_questions(
            self, messages: list, conv_id: str = "", history: list = None, **kwargs
    ):
        # Make history default to empty list if None
        history = history or []
        # Note: conv_id is kept for backward compatibility but is not used for critical functionality
        output_str = ""
        for idx, message in enumerate(messages):
            yield Document(
                channel="thinking",
                content=f"<br><br><b>{message}</b><br><br>"
            )
            # should populate the context
            docs, infos = self.retrieve(message, history)

            yield from infos

            evidence_mode, evidence, images = self.evidence_pipeline(docs).content
            answer = yield from self.answering_pipeline.stream(
                question=message,
                history=history,
                evidence=evidence,
                evidence_mode=evidence_mode,
                images=images,
                conv_id=conv_id,
                channel='thinking',
                **kwargs,
            )

            output_str += (
                f"Sub-question {idx + 1}-th: '{message}'\nAnswer: '{answer.text}'\n\n"
            )

        return output_str

    def stream(  # type: ignore
            self, message: str, conv_id: str = "", history: list = None, **kwargs  # type: ignore
    ) -> Generator[Document, None, Document]:
        # Make history default to empty list if None
        history = history or []

        # Initialize token usage tracking
        model_name = getattr(self.answering_pipeline.llm, "model", "default")
        token_usage = self.init_token_usage_data(model_name, conv_id)

        # Note: conv_id is kept for backward compatibility but is not used for critical functionality
        sub_question_answer_output = ""
        if self.rewrite_pipeline:
            question_tokens = self.count_tokens(message, model_name)
            result = self.rewrite_pipeline(question=message)

            # Track rewrite pipeline token usage
            token_usage["components"]["rewrite_pipeline"]["used"] = True
            token_usage["components"]["rewrite_pipeline"]["prompt_tokens"] = question_tokens

            if isinstance(result, Document):
                message = result.text
                rewrite_result_tokens = self.count_tokens(message, model_name)
                token_usage["components"]["rewrite_pipeline"]["completion_tokens"] = rewrite_result_tokens
                token_usage["components"]["rewrite_pipeline"]["tokens"] = question_tokens + rewrite_result_tokens
            elif (
                    isinstance(result, list)
                    and len(result) > 0
            ):
                # Count tokens for each sub-question
                sub_questions = [r.text for r in result]
                sub_question_tokens = sum(self.count_tokens(q, model_name) for q in sub_questions)
                token_usage["components"]["rewrite_pipeline"]["completion_tokens"] = sub_question_tokens
                token_usage["components"]["rewrite_pipeline"]["tokens"] = question_tokens + sub_question_tokens

                sub_question_answer_output = yield from self.answer_sub_questions(
                    sub_questions, conv_id, history, **kwargs
                )

        # should populate the context
        docs, infos = self.retrieve(message, history)
        # Count tokens in retrieved documents
        doc_tokens = sum(self.count_tokens(doc.text, model_name) for doc in docs)
        token_usage["components"]["retrieve"]["tokens"] = doc_tokens

        yield from infos

        evidence_mode, evidence, images = self.evidence_pipeline(docs).content

        # Count tokens in evidence
        evidence_tokens = self.count_tokens(evidence, model_name)
        sub_qa_tokens = self.count_tokens(sub_question_answer_output, model_name) if sub_question_answer_output else 0
        token_usage["components"]["evidence_pipeline"]["tokens"] = evidence_tokens + sub_qa_tokens

        # Count tokens for answering pipeline
        if hasattr(self.answering_pipeline, "system_prompt") and self.answering_pipeline.system_prompt:
            system_prompt_tokens = self.count_tokens(self.answering_pipeline.system_prompt, model_name)
            token_usage["components"]["answering_pipeline"]["prompt_tokens"] += system_prompt_tokens

        # Count history tokens
        if history:
            history_tokens = sum(self.count_tokens(h, model_name) + self.count_tokens(a, model_name)
                              for h, a in history[-self.answering_pipeline.n_last_interactions:])
            token_usage["components"]["answering_pipeline"]["prompt_tokens"] += history_tokens

        # Count question and evidence tokens
        question_tokens = self.count_tokens(message, model_name)
        token_usage["components"]["answering_pipeline"]["prompt_tokens"] += question_tokens + evidence_tokens + sub_qa_tokens

        def generate_relevant_scores():
            nonlocal docs
            docs = self.retrievers[0].generate_relevant_scores(message, docs)

        # generate relevant score using
        if evidence and self.retrievers:
            scoring_thread = threading.Thread(target=generate_relevant_scores)
            scoring_thread.start()
        else:
            scoring_thread = None

        answer = yield from self.answering_pipeline.stream(
            question=message,
            history=history,
            evidence=evidence + "\n" + sub_question_answer_output,
            evidence_mode=evidence_mode,
            images=images,
            conv_id=conv_id,
            **kwargs,
        )

        # Count completion tokens
        completion_tokens = self.count_tokens(answer.text, model_name)
        token_usage["components"]["answering_pipeline"]["completion_tokens"] = completion_tokens
        token_usage["components"]["answering_pipeline"]["tokens"] = token_usage["components"]["answering_pipeline"]["prompt_tokens"] + completion_tokens

        # Calculate totals including all LLM calls
        token_usage["totals"]["prompt_tokens"] = (
            token_usage["components"]["answering_pipeline"]["prompt_tokens"] +
            (token_usage["components"]["rewrite_pipeline"]["prompt_tokens"] if token_usage["components"]["rewrite_pipeline"]["used"] else 0) +
            (token_usage["components"]["citation_pipeline"]["prompt_tokens"] if token_usage["components"]["citation_pipeline"]["used"] else 0) +
            (token_usage["components"]["mindmap_pipeline"]["prompt_tokens"] if token_usage["components"]["mindmap_pipeline"]["used"] else 0) +
            (token_usage["components"]["add_query_context"]["prompt_tokens"] if token_usage["components"]["add_query_context"]["used"] else 0)
        )
        token_usage["totals"]["completion_tokens"] = (
            token_usage["components"]["answering_pipeline"]["completion_tokens"] +
            (token_usage["components"]["rewrite_pipeline"]["completion_tokens"] if token_usage["components"]["rewrite_pipeline"]["used"] else 0) +
            (token_usage["components"]["citation_pipeline"]["completion_tokens"] if token_usage["components"]["citation_pipeline"]["used"] else 0) +
            (token_usage["components"]["mindmap_pipeline"]["completion_tokens"] if token_usage["components"]["mindmap_pipeline"]["used"] else 0) +
            (token_usage["components"]["add_query_context"]["completion_tokens"] if token_usage["components"]["add_query_context"]["used"] else 0)
        )
        token_usage["totals"]["tokens"] = token_usage["totals"]["prompt_tokens"] + token_usage["totals"]["completion_tokens"]

        # Save token usage to answer metadata and print debug info
        logger.debug(f"[Decompose] Final calculated token_usage before attaching to metadata:\n{json.dumps(token_usage, indent=2)}")
        answer.metadata["token_usage"] = token_usage

        if scoring_thread:
            scoring_thread.join()
        
        # show the evidence
        yield from self.show_citations_and_addons(answer, docs, message)
        # if not with_citation and not without_citation:
        #     yield Document(channel="info", content="<h5><b>No evidence found.</b></h5>")
        # else:
        #     yield Document(channel="info", content=None)
        #     yield from with_citation
        #     yield from without_citation
        
        # <<< ADDED LOGGING >>>
        logger.debug(f"[Decompose] Final answer object metadata before returning from stream. Keys: {list(answer.metadata.keys())}")
        logger.debug(f"[Decompose] token_usage in final answer metadata: {'token_usage' in answer.metadata}")
        # <<< END ADDED LOGGING >>>
        return answer
    
    @classmethod
    def get_user_settings(cls) -> dict:
        user_settings = super().get_user_settings()
        user_settings["decompose_prompt"] = {
            "name": "Decompose Prompt",
            "value": DecomposeQuestionPipeline.DECOMPOSE_SYSTEM_PROMPT_TEMPLATE,
        }
        return user_settings
    
    @classmethod
    def prepare_pipeline_instance(cls, settings, retrievers):
        prefix = f"reasoning.options.{cls.get_info()['id']}"
        pipeline = cls(
            retrievers=retrievers,
            rewrite_pipeline=DecomposeQuestionPipeline(
                prompt_template=settings.get(f"{prefix}.decompose_prompt")
            ),
        )
        return pipeline
    
    @classmethod
    def get_info(cls) -> dict:
        return {
            "id": "complex",
            "name": "Complex QA",
            "description": (
                "Use multi-step reasoning to decompose a complex question into "
                "multiple sub-questions. This pipeline can "
                "perform both keyword search and similarity search to retrieve the "
                "context. After that it includes that context to generate the answer."
            ),
        }
