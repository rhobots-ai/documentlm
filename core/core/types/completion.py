from typing import List, Tuple, Dict, Any, TypedDict


class MindmapNode(TypedDict):
    name: str
    children: List['MindmapNode']


class Mindmap(TypedDict):
    name: str
    children: List[MindmapNode]


class Completion(TypedDict):
    chat_history: List[Tuple[str, str]]
    chat_input: Dict[str, Any]
    file_ids: List[str]
    mindmap: Mindmap
    evidences: List[str]
    selector_output: Dict[str, Any]
    token_usage: Dict[str, Any]
    reason_content: str