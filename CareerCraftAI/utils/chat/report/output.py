from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError

class Reflection(BaseModel):
  missing: str = Field(description="critique of what's missing.")
  superfluous: str = Field(description="critique of what's superfluous.")

class TopicReport(BaseModel):
    """Create Report under the Topic. Provide a Report, reflection, and then follow up with search queries to improve the answer."""

    report: str = Field(description="~200 word detailed report to the job.")
    reflection: Reflection = Field(description="Your reflection on the initial report.")
    search_queries: list[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )