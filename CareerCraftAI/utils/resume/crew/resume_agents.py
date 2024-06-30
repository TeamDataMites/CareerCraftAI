import os
from crewai.agents.executor import TaskEvaluator
from dotenv import load_dotenv
from crewai import Task, Agent, Crew
from crewai.project import CrewBase, agent, task, crew
from langchain_community.retrievers import TavilySearchAPIRetriever
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

from utils.resume.crew.resume_tools import get_linkdin_profile

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")


@CrewBase
class ResumeCrew:
    """Agent that will be used to create Resume."""

    def __init__(self):
        self.agent_config = "../config/agents.yaml"
        self.task_config = "../config/tasks.yaml"
        self.search_retriever = TavilySearchAPIRetriever(k=5, api_key=os.getenv("TAVILY_API_KEY"))
        self.linkdin_retriever = get_linkdin_profile
        self.serper_tool = SerperDevTool()
        self.scrape_website_tool = ScrapeWebsiteTool()

    @agent
    def job_researcher(self) -> Agent:
        return Agent(
            config=self.agent_config['job_researcher'],
            tools=[
                self.search_retriever
            ],
            verbose=True
        )

    @agent
    def personal_profiler(self) -> Agent:
        return Agent(
            config=self.agent_config['personal_profiler'],
            tools=[
                self.linkdin_retriever,
                self.serper_tool,
                self.scrape_website_tool
            ],
            verbose=True
        )

    @agent
    def resume_strategist(self) -> Agent:
        return Agent(
            config=self.agent_config['resume_strategist'],
            verbose=True
        )
    
    @agent 
    def interview_preparer(self) -> Agent:
        return Agent(
            config=self.agent_config['interview_preparer'],
            tools=[
                self.search_retriever
            ],
            verbose=True
        )

    @agent
    def resume_editor(self) -> Agent:
        return Agent(
            config=self.agent_config['resume_editor'],
            verbose=True
        )

    @task
    def research_jobs(self) -> Task:
        return Task(
            config=self.task_config['research_jobs'],

        )

    @task
    def create_personal_profile(self) -> Task:
        return Task(
            config=self.task_config['create_personal_profile'],
        )

    @task
    def create_resume_strategy(self) -> Task:
        return Task(
            config=self.task_config['create_resume_strategy'],
        )

    @task
    def write_resume(self) -> Task:
        return Task(
            config=self.task_config['write_resume']
        )

    @task
    def edit_resume(self) -> Task:
        return Task(
            config=self.task_config['edit_resume']
        )

    @task
    def quality_control(self) -> Task:
        return Task(
            config=self.task_config['quality_control']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.job_researcher,
                self.personal_profiler,
                self.resume_strategist,
                self.resume_editor
            ],
            tasks=[
                self.research_jobs,
                self.create_personal_profile,
                self.create_resume_strategy,
                self.write_resume,
                self.edit_resume,
                self.quality_control
            ],
            verbose=True
        )
