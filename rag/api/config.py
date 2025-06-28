"""Configuration settings for the Flask API."""
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Default settings for document upload and chat
DEFAULT_SETTINGS = {
    "index.options.1.reader_mode": "default",
    "index.options.1.reranking_llm": "openai",
    "index.options.1.num_retrieval": 10,
    "index.options.1.retrieval_mode": "hybrid",
    "index.options.1.prioritize_table": False,
    "index.options.1.mmr": False,
    "index.options.1.use_reranking": True,
    "index.options.1.use_llm_reranking": True,
    "reasoning.use": "simple",
    "reasoning.lang": "en",
    "reasoning.max_context_length": 32000,
    "reasoning.options.simple.llm": "openai",
    "reasoning.options.simple.highlight_citation": "highlight",
    "reasoning.options.simple.create_mindmap": True,
    "reasoning.options.simple.create_citation_viz": False,
    "reasoning.options.simple.use_multimodal": False,
    "reasoning.options.simple.system_prompt": "This is a question answering system.",
    "reasoning.options.simple.qa_prompt": "Use the following pieces of context to answer the question at the end in detail with clear explanation. If you don't know the answer, just say that you don't know, don't try to make up an answer. If the question or user input is irrelevant, respond in natural language. Give answer in {lang}.\n\n{context}\nQuestion/User Input: {question}\nHelpful Answer:",
    "reasoning.options.simple.n_last_interactions": 5,
    "reasoning.options.simple.trigger_context": 150,
    "reasoning.options.complex.llm": "",
    "reasoning.options.complex.highlight_citation": "highlight",
    "reasoning.options.complex.create_mindmap": False,
    "reasoning.options.complex.create_citation_viz": False,
    "reasoning.options.complex.use_multimodal": False,
    "reasoning.options.complex.system_prompt": "This is a question answering system.",
    "reasoning.options.complex.qa_prompt": "Use the following pieces of context to answer the question at the end in detail with clear explanation. If you don't know the answer, just say that you don't know, don't try to make up an answer. Give answer in {lang}.\n\n{context}\nQuestion: {question}\nHelpful Answer:",
    "reasoning.options.complex.n_last_interactions": 5,
    "reasoning.options.complex.trigger_context": 150,
    "reasoning.options.complex.decompose_prompt": "You are an expert at converting user complex questions into sub questions. Perform query decomposition using provided function_call. Given a user question, break it down into the most specific sub questions you can (at most 3) which will help you answer the original question. Each sub question should be about a single concept/fact/idea. If there are acronyms or words you are not familiar with, do not try to rephrase them.",
    "reasoning.options.ReAct.llm": "",
    "reasoning.options.ReAct.tools": [
        "SearchDoc",
        "LLM"
    ],
    "reasoning.options.ReAct.max_iterations": 5,
    "reasoning.options.ReAct.qa_prompt": "Answer the following questions as best you can. Give answer in {lang}. You have access to the following tools:\n{tool_description}\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\n\nAction: the action to take, should be one of [{tool_names}]\n\nAction Input: the input to the action, should be different from the action input of the same action in previous steps.\n\nObservation: the result of the action\n\n... (this Thought/Action/Action Input/Observation can repeat N times)\n#Thought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin! After each Action Input.\n\nQuestion: {instruction}\nThought: {agent_scratchpad}\n",
    "reasoning.options.ReWOO.planner_llm": "",
    "reasoning.options.ReWOO.solver_llm": "",
    "reasoning.options.ReWOO.highlight_citation": False,
    "reasoning.options.ReWOO.tools": [
        "SearchDoc",
        "LLM"
    ],
    "reasoning.options.ReWOO.planner_prompt": "You are an AI agent who makes step-by-step plans to solve a problem under the help of external tools. For each step, make one plan followed by one tool-call, which will be executed later to retrieve evidence for that step.\nYou should store each evidence into a distinct variable #E1, #E2, #E3 ... that can be referred to in later tool-call inputs.\n\n##Available Tools##\n{tool_description}\n\n##Output Format (Replace '<...>')##\n#Plan1: <describe your plan here>\n#E1: <toolname>[<input here>] (eg. Search[What is Python])\n#Plan2: <describe next plan>\n#E2: <toolname>[<input here, you can use #E1 to represent its expected output>]\nAnd so on...\n\n##Your Task##\n{task}\n\n##Now Begin##\n",
    "reasoning.options.ReWOO.solver_prompt": "You are an AI agent who solves a problem with my assistance. I will provide step-by-step plans(#Plan) and evidences(#E) that could be helpful.\nYour task is to briefly summarize each step, then make a short final conclusion for your task. Give answer in {lang}.\n\n##My Plans and Evidences##\n{plan_evidence}\n\n##Example Output##\nFirst, I <did something> , and I think <...>; Second, I <...>, and I think <...>; ....\nSo, <your conclusion>.\n\n##Your Task##\n{task}\n\n##Now Begin##\n"
}
