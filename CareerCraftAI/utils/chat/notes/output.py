from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic.v1 import validator
from typing import List, Optional


class Subsection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    description: str = Field(..., title="Content of the subsection")

    @property
    def as_str(self) -> str:
        return f"### {self.subsection_title}\n\n{self.description}".strip()
    

class Section(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    description: str = Field(..., title="Content of the section")
    subsections: Optional[List[Subsection]] = Field(
        default=None,
        title="Titles and descriptions for each subsection of the Lecture.",
    )

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(
            f"### {subsection.subsection_title}\n\n{subsection.description}"
            for subsection in self.subsections or []
        )
        return f"## {self.section_title}\n\n{self.description}\n\n{subsections}".strip()
    

class Outline(BaseModel):
    page_title: str = Field(..., title="Title of the Lecture")
    sections: List[Section] = Field(
        default_factory=list,
        title="Titles and descriptions for each section of the Lecture.",
    )

    @property
    def as_str(self) -> str:
        sections = "\n\n".join(section.as_str for section in self.sections)
        return f"# {self.page_title}\n\n{sections}".strip()
    

class RelatedSubjects(BaseModel):
    topics: List[str] = Field(
        description="Comprehensive list of related subjects as background research.",
    )


class Editor(BaseModel):
  affiliation: str = Field(..., title="Primary Affiliation of the editor")
  name: str = Field(..., title="Name of the editor",  pattern=r"^[a-zA-Z0-9_-]{1,64}$")
  role: str = Field(..., title="Role of the editor in context of the topic",  pattern=r"^[a-zA-Z0-9_-]{1,64}$")
  description: str = Field(
        description="Description of the editor's focus, concerns, and motives.",
    )

  @property
  def persona(self) -> str:
    return f"Name: {self.name}\nRole: {self.role}\nAffiliation: {self.affiliation}\nDescription: {self.description}\n"
  

class Perspectives(BaseModel):
    editors: List[Editor] = Field(
        description="Comprehensive list of editors with their roles and affiliations.",
        max_items=8, min_items=5
    )

    @validator('editors')
    @classmethod
    def validate_editors(cls, editors):
        if len(editors) < 5:
            raise ValueError("At least 5 editors are required.")
        return editors


class Queries(BaseModel):
    queries: List[str] = Field(
        description="Comprehensive list of search engine queries to answer the user's questions.",
    )


class AnswerWithCitations(BaseModel):
    answer: str = Field(
        description="Comprehensive answer to user's question with citation.",
    )
    cited_urls: List[str] = Field(
        description="List of url's for citations for the answer.",
    )

    @property
    def as_str(self) -> str:
        return f"{self.answer}\n\nCitations:\n\n" + "\n".join(
            f"[{i+1}]: {url}" for i, url in enumerate(self.cited_urls)
        )


class LectureSubSection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    content: str = Field(
        ...,
        title="Full content of the subsection. Include [#] citations to the cited sources where relevant.",
    )

    @property
    def as_str(self) -> str:
        return f"### {self.subsection_title}\n\n{self.content}".strip()


class LectureSection(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    content: str = Field(..., title="Full content of the section")
    subsections: Optional[List[LectureSubSection]] = Field(
        default=None,
        title="Titles and descriptions for each subsection of the Lecture.",
    )
    citations: List[str] = Field(default_factory=list)

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(
            subsection.as_str for subsection in self.subsections or []
        )
        citations = "\n".join([f" [{i}] {cit}" for i, cit in enumerate(self.citations)])
        return (
            f"## {self.section_title}\n\n{self.content}\n\n{subsections}".strip()
            + f"\n\n{citations}".strip()
        )
