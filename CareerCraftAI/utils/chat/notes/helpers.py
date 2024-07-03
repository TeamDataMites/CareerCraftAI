from typing import List, Optional, TypedDict, Annotated
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage
from utils.chat.notes.output import Outline, LectureSection
from utils.chat.notes.output import Editor

def add_messages(left, right):
  if not isinstance(left, list):
    left = [left]
  if not isinstance(right, list):
    right = [right]
  return left + right

def update_references(references, new_references):
  if not references:
    references = {}
  references.update(new_references)
  return references

def update_editor(editor, new_editor):
    # Can only set at the outset
    if not editor:
        return new_editor
    return editor

class InterviewState(TypedDict):
    messages: Annotated[List[AnyMessage], add_messages]
    references: Annotated[Optional[dict], update_references]
    editor: Annotated[Optional[Editor], update_editor]

def tag_with_name(ai_message: AIMessage, name: str):
    ai_message.name = name
    return ai_message


def swap_roles(state: InterviewState, name: str):
    converted = []
    for message in state["messages"]:
        if isinstance(message, AIMessage) and message.name != name:
            message = HumanMessage(**message.dict(exclude={"type"}))
        converted.append(message)
    return {"messages": converted}

class ResearchState(TypedDict):
    topic: str
    domain: str
    outline: Outline
    editors: List[Editor]
    interview_results: List[InterviewState]
    # The final sections output
    sections: List[LectureSection]
    article: str
