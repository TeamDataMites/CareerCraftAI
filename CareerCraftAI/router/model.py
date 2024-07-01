import os
from fastapi import APIRouter, BackgroundTasks
from schemas.item import PersonalData
from utils.chat.mindmap.agent import mindmap_agent
from utils.resume.crew.resume_run import resume_crew
from utils.chat.report.agent import run_report_agent

router = APIRouter(
    prefix="/prediction",
    tags=["models"]
)


@router.get("/mindmap/", 
            description="Generate a mindmap from a job description.", 
            summary="endpoint access the llm agents to generate mindmap"
            )
async def mindmap(desc: str):
    mermaid_code: str = mindmap_agent(
        desc
    )
    return {"code": mermaid_code}


@router.get('/cv/',
            description="fine-tune the cv",
            summary="endpoint to use cv finetune in the background"
            )
async def finetune(personalData: PersonalData, background_tasks: BackgroundTasks):
    background_tasks.add_task(resume_crew, 
                              linkdin_url=personalData.linkdin_url, 
                              github_url=personalData.github_url, 
                              personal_writeup=personalData.personal_writeup, 
                              job_post=personalData.job_post, 
                              resume=personalData.resume
                            )
    return {"message": "background task started for cv task"}


@router.get(
        "/result/",
        description="fine-tune the cv",
        summary="endpoint to get cv finetune"
         )
async def get_result():
    if os.path.exists('resume.md'):
        with open('resume.md', "r") as file:
            content = file.read()
        return {"result": content}
    return {"result": "Analysis not complete or file not found"}


@router.get(
    "/load_direct/",
    description="fine-tune the cv",
    summary="endpoint to load cv finetune directly"
)
async def get_cv(personalData: PersonalData):
    result = resume_crew(
        linkdin_url=personalData.linkdin_url, 
        github_url=personalData.github_url, 
        personal_writeup=personalData.personal_writeup, 
        job_post=personalData.job_post, 
        resume=personalData.resume
    )

    return {"result": result}

@router.get('/job_report/',
            description="get detailed report on the job and company given a description",
            summary="job report"
            )
async def get_job_report(desc: str):
    report = await run_report_agent(desc)
    return {"report": report}

@router.post('/lecture_note/', 
            summary="AI generated lecture note",
            description="provides a extensivly researched not on a topic of interest."
            )
async def generate_lecture(topic: str):
    pass



