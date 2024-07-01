import os
from dotenv import load_dotenv
from crewai import Task, Agent, Crew
from crewai.project import CrewBase, agent, task, crew
from langchain_community.tools.tavily_search import TavilySearchResults
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

from utils.resume.crew.resume_tools import get_linkdin_profile
from langchain_openai import ChatOpenAI

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


@CrewBase
class ResumeCrew:
    """Agent that will be used to create Resume."""

    def __init__(self):
        self.agents_config = "config/agents.yaml"
        self.tasks_config = "config/tasks.yaml"
        self.search_retriever = TavilySearchResults(k=3, api_key=os.getenv("TAVILY_API_KEY"))
        self.linkdin_retriever = get_linkdin_profile
        self.serper_tool = SerperDevTool()
        self.scrape_website_tool = ScrapeWebsiteTool()
        self.llm = ChatOpenAI(model='gpt-3.5-turbo')
        self.tool_llm = ChatOpenAI(model='gpt-4o')

    @agent
    def job_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['job_researcher'],
            tools=[
                self.search_retriever
            ],
            llm=self.llm,
            verbose=True,
            max_iter=5
        )

    @agent
    def personal_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config['personal_profiler'],
            tools=[
                self.linkdin_retriever,
                self.serper_tool,
                self.scrape_website_tool
            ],
            llm=self.tool_llm,
            verbose=True,
            max_iter=5
        )

    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_strategist'],
            verbose=True,
            llm=self.tool_llm
        )

    @agent
    def resume_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_editor'],
            verbose=True,
            llm=self.llm,
        )

    @task
    def research_jobs(self) -> Task:
        return Task(
            config=self.tasks_config['research_jobs'],
            agent=self.job_researcher(),
            async_execution=True
        )

    @task
    def create_personal_profile(self) -> Task:
        return Task(
            config=self.tasks_config['create_personal_profile'],
            agent=self.personal_profiler(),
            async_execution=True
        )

    @task
    def create_resume_strategy(self) -> Task:
        return Task(
            config=self.tasks_config['create_resume_strategy'],
            agent=self.resume_strategist(),
            output_file="resume.md",
            context=[self.research_jobs(), self.create_personal_profile()],
        )

    @task
    def quality_control(self) -> Task:
        return Task(
            config=self.tasks_config['quality_control'],
            agent=self.resume_editor(),
            context=[self.create_resume_strategy()],
            output_file="resume-final.md"
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )
