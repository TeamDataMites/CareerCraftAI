import os
from fastapi import APIRouter, BackgroundTasks
from schemas.item import PersonalData
from utils.chat.mindmap.agent import mindmap_agent
from utils.resume.crew.resume_run import resume_crew, resume_save
from utils.chat.report.agent import run_report_agent
from database.database import db

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


@router.post('/cv/',
            description="fine-tune the cv",
            summary="endpoint to use cv finetune in the background"
            )
async def finetune(personalData: PersonalData, background_tasks: BackgroundTasks, task_name: str = "cv_task"):
    background_tasks.add_task(resume_save,
                              name=personalData.task_name, 
                              linkdin_url=personalData.linkdin_url, 
                              github_url=personalData.github_url, 
                              personal_writeup=personalData.personal_writeup, 
                              job_post=personalData.job_post, 
                              resume=personalData.resume
                            )
    
    return {"message": "background task started for cv task", "taskId": task_name}


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


@router.get('/cv/{task_name}', description="get finetuned cv from firestore")
async def get_cv(task_name: str):
    task_doc = db.collection('tasks').document(task_name).get()
    if not task_doc.exists:
        return {"status": "not found"}
    
    task_data = task_doc.to_dict()
    
    if task_data['status'] == 'completed':
        return {"status": "completed", "result": task_data['result']}
    
    return {"status": task_data['status']}


@router.post(
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
async def get_job_report(job_poster: str, desc: str):
    description: str = f"Posted by: {job_poster} \n\n {desc}"
    report = run_report_agent(description)
    return {"report": report}


@router.get('/lecture_note/', 
            summary="AI generated lecture note",
            description="provides a extensivly researched not on a topic of interest."
            )
async def generate_lecture(topic: str, domain: str):
    pass
