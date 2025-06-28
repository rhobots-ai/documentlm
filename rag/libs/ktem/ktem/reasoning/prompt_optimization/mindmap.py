import logging
from textwrap import dedent

from ktem.llms.manager import llms

from kotaemon.base import BaseComponent, Document, HumanMessage, Node, SystemMessage
from kotaemon.llms import ChatLLM, PromptTemplate

logger = logging.getLogger(__name__)


MINDMAP_HTML_EXPORT_TEMPLATE = dedent(
    """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mindmap</title>
    <style>
      svg.markmap {
        width: 100%;
        height: 100vh;
      }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.16"></script>
  </head>
  <body>
    {markmap_div}
  </body>
</html>
"""
)


class CreateMindmapPipeline(BaseComponent):
    """Create a mindmap from the question and context"""

    llm: ChatLLM = Node(default_callback=lambda _: llms.get_default())

    SYSTEM_PROMPT = """
From now on you will behave as "MapGPT" and, for every text the user will submit, you are going to create a PlantUML mind map file for the inputted text to best describe main ideas. Format it as a code and remember that the mind map should be in the same language as the inputted context. You don't have to provide a general example for the mind map format before the user inputs the text.
    """  # noqa: E501
    MINDMAP_PROMPT_TEMPLATE = """
Question:
{question}

Context:
{context}

Generate a sample PlantUML mindmap for based on the provided question and context above. Only includes context relevant to the question to produce the mindmap.

Use the template like this:

@startmindmap
* Title
** Item A
*** Item B
**** Item C
*** Item D
@endmindmap
    """  # noqa: E501
    prompt_template: str = MINDMAP_PROMPT_TEMPLATE

    @classmethod
    def convert_uml_to_markdown(cls, text: str) -> str:
        start_phrase = "@startmindmap"
        end_phrase = "@endmindmap"

        try:
            text = text.split(start_phrase)[-1]
            text = text.split(end_phrase)[0]
            text = text.strip().replace("*", "#")
        except IndexError:
            text = ""

        return text
        
    @classmethod
    def convert_to_json(cls, markdown_text: str) -> dict:
        """Convert markdown hierarchical list to JSON tree structure."""
        if not markdown_text or not markdown_text.strip():
            return {"name": "No content", "children": []}
        
        lines = markdown_text.strip().split('\n')
        
        # Create root node
        tree = {"name": "Root", "children": []}
        
        # Stack to keep track of parent nodes at each level
        node_stack = [tree]
        current_levels = [0]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Count # symbols to determine level
            level = 0
            for char in line:
                if char == '#':
                    level += 1
                else:
                    break
            
            # Extract the node text (removing leading # symbols)
            node_text = line[level:].strip()
            if not node_text:
                continue
                
            # Create new node
            new_node = {"name": node_text, "children": []}
            
            # Find appropriate parent based on level
            while len(current_levels) > 1 and level <= current_levels[-1]:
                node_stack.pop()
                current_levels.pop()
            
            # Add as child to current parent
            node_stack[-1]["children"].append(new_node)
            
            # Push onto stack to become potential parent
            node_stack.append(new_node)
            current_levels.append(level)
        
        # If the root only has one child and no content itself, return just the child
        if len(tree["children"]) == 1 and tree["name"] == "Root":
            return tree["children"][0]
        
        return tree

    def run(self, question: str, context: str) -> Document:  # type: ignore
        prompt_template = PromptTemplate(self.prompt_template)
        prompt = prompt_template.populate(
            question=question,
            context=context,
        )

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        uml_text = self.llm(messages).text
        markdown_text = self.convert_uml_to_markdown(uml_text)
        
        # Generate JSON representation
        json_structure = self.convert_to_json(markdown_text)

        return Document(
            text=markdown_text,
            metadata={"json_structure": json_structure}
        )
