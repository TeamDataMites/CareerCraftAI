import os
import dotenv
from langchain_core.messages import ToolMessage
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError

dotenv.load_dotenv()
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')

class Reflection(BaseModel):
  missing: str = Field(description="critique of what's missing.")
  superfluous: str = Field(description="critique of what's superfluous.")

class TopicReport(BaseModel):
    """Create Report under the Topic. Provide a Report, reflection, and then follow up with search queries to improve the answer."""

    report: str = Field(description="~500 word detailed report to the job.")
    reflection: Reflection = Field(description="Your reflection on the initial report.")
    search_queries: list[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )
class ReviseAnswer(TopicReport):
    """Revise your original answer to your question. Provide an answer, reflection,

    cite your reflection with references, and finally
    add search queries to improve the answer."""

    references: list[str] = Field(
        description="Citations motivating your updated answer."
    )


class ResponderWithRetries:
    def __init__(self, runnable, validator):
        self.runnable = runnable
        self.validator = validator

    def respond(self, state: list):
        response = []
        for attempt in range(3):
            response = self.runnable.invoke(
                {"messages": state}, {"tags": [f"attempt:{attempt}"]}
            )
            try:
                self.validator.invoke(response)
                return response
            except ValidationError as e:
                state = state + [
                    response,
                    ToolMessage(
                        content=f"{repr(e)}\n\nPay close attention to the function schema.\n\n"
                        + self.validator.schema_json()
                        + " Respond by fixing all validation errors.",
                        tool_call_id=response.tool_calls[0]["id"],
                    ),
                ]
        return response
    