import re
import threading
import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Generator, Dict, Any, Optional

import numpy as np
import tiktoken

from kotaemon.base import AIMessage, Document, HumanMessage, SystemMessage
from kotaemon.llms import PromptTemplate

logger = logging.getLogger(__name__)

from .citation_qa import (
    CITATION_TIMEOUT,
    MAX_IMAGES,
    AnswerWithContextPipeline,
    CONTEXT_RELEVANT_WARNING_SCORE,
)
from .format_context import EVIDENCE_MODE_FIGURE
from .utils import find_start_end_phrase
from libs.ktem.ktem.utils.render import Render

DEFAULT_QA_CITATION_PROMPT = """
Use the following pieces of context to answer the question at the end in detail with clear explanation.
Format answer with easy to follow bullets / paragraphs.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use the same language as the question to response.

CONTEXT:
----
{context}
----

Answer using this format:
CITATION LIST

// the index in this array
CITATION【number】

// output 2 phrase to mark start and end of the relevant span
// each has ~ 6 words
// MUST COPY EXACTLY from the CONTEXT
// NO CHANGE or REPHRASE
// RELEVANT_SPAN_FROM_CONTEXT
START_PHRASE: string
END_PHRASE: string

// When you answer, ensure to add citations from the documents
// in the CONTEXT with a number that corresponds to the answersInText array.
// (in the form [number])
// Try to include the number after each facts / statements you make.
// You can create as many citations as you need.
FINAL ANSWER
string

STRICTLY FOLLOW THIS EXAMPLE:
CITATION LIST

CITATION【1】

START_PHRASE: Known as fixed-size chunking , the traditional
END_PHRASE: not degrade the final retrieval performance.

CITATION【2】

START_PHRASE: Fixed-size Chunker This is our baseline chunker
END_PHRASE: this shows good retrieval quality.

FINAL ANSWER
An alternative to semantic chunking is fixed-size chunking. This traditional method involves splitting documents into chunks of a predetermined or user-specified size, regardless of semantic content, which is computationally efficient【1】. However, it may result in the fragmentation of semantically related content, thereby potentially degrading retrieval performance【1】【2】.

QUESTION: {question}\n
ANSWER:
"""  # noqa

START_ANSWER = "FINAL ANSWER"
START_CITATION = "CITATION LIST"
CITATION_PATTERN = r"citation【(\d+)】"
START_ANSWER_PATTERN = "start_phrase:"
END_ANSWER_PATTERN = "end_phrase:"


@dataclass
class InlineEvidence:
	"""List of evidences to support the answer."""
	
	start_phrase: str | None = None
	end_phrase: str | None = None
	idx: int | None = None


class AnswerWithInlineCitation(AnswerWithContextPipeline):
	"""Answer the question based on the evidence with inline citation"""
	
	qa_citation_template: str = DEFAULT_QA_CITATION_PROMPT
	
	def count_tokens(self, text: str, model_name: str = None) -> int:
		"""Count tokens in a string using tiktoken"""
		if not text:
			return 0
		
		try:
			if not model_name or model_name == "default":
				# Default to gpt-3.5-turbo if no model specified
				tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
			# For OpenAI models
			elif model_name.startswith(("gpt-", "text-embedding-")):
				tokenizer = tiktoken.encoding_for_model(model_name)
			# For other models - fallback to cl100k_base
			else:
				tokenizer = tiktoken.get_encoding("cl100k_base")
			
			return len(tokenizer.encode(str(text)))
		except Exception as e:
			logger.warning(f"Error counting tokens for {model_name}: {str(e)}")
			# Fallback to an approximation if tiktoken fails
			return len(str(text).split()) * 1.3  # Rough approximation
	
	def get_prompt(self, question, evidence, evidence_mode: int):
		"""Prepare the prompt and other information for LLM"""
		prompt_template = PromptTemplate(self.qa_citation_template)
		
		prompt = prompt_template.populate(
			context=evidence,
			question=question,
			safe=False,
		)
		
		return prompt, evidence
	
	def answer_to_citations(self, answer) -> list[InlineEvidence]:
		citations: list[InlineEvidence] = []
		lines = answer.split("\n")
		
		current_evidence = None
		
		for line in lines:
			# check citation idx using regex
			match = re.match(CITATION_PATTERN, line.lower())
			
			if match:
				try:
					parsed_citation_idx = int(match.group(1))
				except ValueError:
					parsed_citation_idx = None
				
				# conclude the current evidence if exists
				if current_evidence:
					citations.append(current_evidence)
					current_evidence = None
				
				current_evidence = InlineEvidence(idx=parsed_citation_idx)
			else:
				for keyword in [START_ANSWER_PATTERN, END_ANSWER_PATTERN]:
					if line.lower().startswith(keyword):
						matched_phrase = line[len(keyword):].strip()
						if not current_evidence:
							current_evidence = InlineEvidence(idx=None)
						
						if keyword == START_ANSWER_PATTERN:
							current_evidence.start_phrase = matched_phrase
						else:
							current_evidence.end_phrase = matched_phrase
						
						break
			
			if (
					current_evidence
					and current_evidence.end_phrase
					and current_evidence.start_phrase
			):
				citations.append(current_evidence)
				current_evidence = None
		
		if current_evidence:
			citations.append(current_evidence)
		
		return citations
	
	def replace_citation_with_link(self, answer: str):
		# Define the regex pattern to match 【number】
		pattern = r"【\d+】"
		alternate_pattern = r"\[\d+\]"
		
		# Regular expression to match merged citations
		multi_pattern = r"【([\d,\s]+)】"
		
		# Function to replace merged citations with independent ones
		def split_citations(match):
			# Extract the numbers, split by comma, and create individual citations
			numbers = match.group(1).split(",")
			return "".join(f"【{num.strip()}】" for num in numbers)
		
		# Replace merged citations in the text
		answer = re.sub(multi_pattern, split_citations, answer)
		
		# Find all citations in the answer
		matches = list(re.finditer(pattern, answer))
		if not matches:
			matches = list(re.finditer(alternate_pattern, answer))
		
		matched_citations = set()
		for match in matches:
			citation = match.group()
			matched_citations.add(citation)
		
		for citation in matched_citations:
			citation_id = citation[1:-1]
			
			# Create a link that points to the citation document and has a mark-{citation_id} ID
			# This connects the in-text citation with the document reference
			answer = answer.replace(
				citation,
				(
					f'<a href="#citation-{citation_id}" class="citation" '
					f'id="mark-{citation_id}">【{citation_id}】</a>'
				),
			)
		
		answer = answer.replace(START_CITATION, "")
		
		logger.info(f"Processed {len(matched_citations)} inline citations in the answer")
		return answer
	
	def stream(  # type: ignore
			self,
			question: str,
			evidence: str,
			evidence_mode: int = 0,
			images: list[str] = [],
			**kwargs,
	) -> Generator[Document, None, Document]:
		history = kwargs.get("history", [])
		channel = kwargs.get("channel", 'chat')
		# check if evidence exists, use QA prompt
		if evidence:
			prompt, evidence = self.get_prompt(question, evidence, evidence_mode)
		else:
			prompt = question
		
		output = ""
		logprobs = []
		
		citation = None
		mindmap = None
		
		def mindmap_call():
			nonlocal mindmap
			mindmap = self.create_mindmap_pipeline(context=evidence, question=question)
		
		mindmap_thread = None
		
		# execute function call in thread
		if evidence:
			if self.enable_mindmap:
				mindmap_thread = threading.Thread(target=mindmap_call)
				mindmap_thread.start()
		
		messages = []
		if self.system_prompt:
			messages.append(SystemMessage(content=self.system_prompt))
		
		for human, ai in history[-self.n_last_interactions:]:
			messages.append(HumanMessage(content=human))
			messages.append(AIMessage(content=ai))
		
		if self.use_multimodal and evidence_mode == EVIDENCE_MODE_FIGURE:
			# create image message:
			messages.append(
				HumanMessage(
					content=[
						        {"type": "text", "text": prompt},
					        ]
					        + [
						        {
							        "type": "image_url",
							        "image_url": {"url": image},
						        }
						        for image in images[:MAX_IMAGES]
					        ],
				)
			)
		else:
			# append main prompt
			messages.append(HumanMessage(content=prompt))
		
		final_answer = ""
		
		try:
			# try streaming first
			print("Trying LLM streaming")
			for out_msg in self.llm.stream(messages):
				if evidence:
					if START_ANSWER in output:
						if not final_answer:
							try:
								left_over_answer = output.split(START_ANSWER)[
									1
								].lstrip()
							except IndexError:
								left_over_answer = ""
							if left_over_answer:
								out_msg.text = left_over_answer + out_msg.text
						
						final_answer += (
							out_msg.text.lstrip() if not final_answer else out_msg.text
						)
						yield Document(channel=channel, content=out_msg.text)
						
						# check for the edge case of citation list is repeated
						# with smaller LLMs
						if START_CITATION in out_msg.text:
							break
				else:
					yield Document(channel=channel, content=out_msg.text)
				
				output += out_msg.text
				logprobs += out_msg.logprobs
		except NotImplementedError:
			print("Streaming is not supported, falling back to normal processing")
			output = self.llm(messages).text
			yield Document(channel=channel, content=output)
		
		if logprobs:
			qa_score = np.exp(np.average(logprobs))
		else:
			qa_score = None
		
		citation = self.answer_to_citations(output)
		
		if mindmap_thread:
			mindmap_thread.join(timeout=CITATION_TIMEOUT)

		answer = Document(
			text=output,
			metadata={
				"citation_viz": self.enable_citation_viz,
				"mindmap": mindmap,
				"citation": citation,
				"qa_score": qa_score,
			},
		)
		
		return answer

	def prepare_citations(self, answer, docs) -> tuple[list[Document], list[Document], list[Document], list[Document]]:
		"""Prepare the citations to show on the UI"""
		with_citation, without_citation, raw_with_citation, raw_without_citation = [], [], [], []
		has_llm_score = any("llm_trulens_score" in doc.metadata for doc in docs)

		spans = self.match_evidence_with_context(answer, docs)
		id2docs = {doc.doc_id: doc for doc in docs}
		not_detected = set(id2docs.keys()) - set(spans.keys())

		# render highlight spans
		for _id, ss in spans.items():
			if not ss:
				not_detected.add(_id)
				continue
			cur_doc = id2docs[_id]
			highlight_text = ""

			ss = sorted(ss, key=lambda x: x["start"])
			last_end = 0
			text = cur_doc.text[: ss[0]["start"]]

			for idx, span in enumerate(ss):
				# prevent overlapping between span
				span_start = max(last_end, span["start"])
				span_end = max(last_end, span["end"])

				to_highlight = cur_doc.text[span_start:span_end]
				last_end = span_end

				# append to highlight on PDF viewer
				highlight_text += (" " if highlight_text else "") + to_highlight

				span_idx = span.get("idx", None)
				if span_idx is not None:
					to_highlight = f"【{span_idx}】" + to_highlight

				text += Render.highlight(
					to_highlight,
					elem_id=str(span_idx) if span_idx is not None else None,
				)
				if idx < len(ss) - 1:
					text += cur_doc.text[span["end"] : ss[idx + 1]["start"]]

			text += cur_doc.text[ss[-1]["end"] :]
			# add to display list
			with_citation.append(
				Document(
					channel="info",
					content=Render.collapsible_with_header_score(
						cur_doc,
						override_text=text,
						highlight_text=highlight_text,
						open_collapsible=True,
					),
				)
			)

			raw_with_citation.append(
				Document(
					channel="info",
					content={
						'doc': cur_doc,
						'override_text': text,
						'highlight_text': highlight_text,
						'has_citations': True
					}
				)
			)

		sorted_not_detected_items_with_scores = [
			(id_, id2docs[id_].metadata.get("llm_trulens_score", 0.0))
			for id_ in not_detected
		]
		sorted_not_detected_items_with_scores.sort(key=lambda x: x[1], reverse=True)

		for id_, _ in sorted_not_detected_items_with_scores:
			doc = id2docs[id_]
			doc_score = doc.metadata.get("llm_trulens_score", 0.0)
			is_open = not has_llm_score or (
					doc_score
					> CONTEXT_RELEVANT_WARNING_SCORE
				# and len(with_citation) == 0
			)
			without_citation.append(
				Document(
					channel="info",
					content=Render.collapsible_with_header_score(
						doc, open_collapsible=is_open
					),
				)
			)

			raw_without_citation.append(
				Document(
					channel="info",
					content={
						'doc': doc,
						'has_citations': False
					}
				)
			)
		return with_citation, without_citation, raw_with_citation, raw_without_citation
	
	def log_citation_info(self, answer, docs, with_citation) -> None:
		"""Log detailed information about citations for debugging"""
		try:
			citation_list = answer.metadata.get("citation", [])
			
			logger.info(f"=== INLINE CITATION DEBUG INFO ===")
			logger.info(f"Total citations in answer metadata: {len(citation_list)}")
			logger.info(f"Total citation documents generated: {len(with_citation)}")
			
			# Log each citation from answer metadata
			for i, citation in enumerate(citation_list):
				idx = citation.idx if citation.idx is not None else i+1
				logger.info(f"Citation {idx}:")
				logger.info(f"  Start phrase: '{citation.start_phrase}'")
				logger.info(f"  End phrase: '{citation.end_phrase}'")
			
			# Log document search results 
			spans = self.match_evidence_with_context(answer, docs)
			logger.info(f"Documents matched with citations: {len(spans)}")
			for doc_id, span_infos in spans.items():
				logger.info(f"Document {doc_id}: {len(span_infos)} spans matched")
				for span in span_infos:
					logger.info(f"  Span: citation idx={span.get('idx')}, start={span.get('start')}, end={span.get('end')}")
					
			logger.info(f"=== END DEBUG INFO ===")
		except Exception as e:
			logger.error(f"Error in debug logging: {str(e)}")
	
	def match_evidence_with_context(self, answer, docs) -> dict[str, list[dict]]:
		"""Match the evidence with the context"""
		spans: dict[str, list[dict]] = defaultdict(list)
		
		if not answer.metadata.get("citation"):
			logger.warning("No citations found in answer metadata")
			return spans
		
		evidences = answer.metadata["citation"]
		
		for e_id, evidence in enumerate(evidences):
			start_phrase, end_phrase = evidence.start_phrase, evidence.end_phrase
			evidence_idx = evidence.idx
			
			if evidence_idx is None:
				evidence_idx = e_id + 1
			
			best_match = None
			best_match_length = 0
			best_match_doc_idx = None
			
			for doc in docs:
				match, match_length = find_start_end_phrase(
					start_phrase, end_phrase, doc.text
				)
				if best_match is None or (
						match is not None and match_length > best_match_length
				):
					best_match = match
					best_match_length = match_length
					best_match_doc_idx = doc.doc_id
			
			if best_match is not None and best_match_doc_idx is not None:
				spans[best_match_doc_idx].append(
					{
						"start": best_match[0],
						"end": best_match[1],
						"idx": evidence_idx,
					}
				)
		return spans
