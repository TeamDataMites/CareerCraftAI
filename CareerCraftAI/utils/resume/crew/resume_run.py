from utils.resume.crew.resume_agents import ResumeCrew
from database.database import db

def resume_crew(linkdin_url, github_url, personal_writeup, job_post, resume):
    inputs = {
        'linkdin_url': linkdin_url,
        'github_url': github_url,
        'personal_writeup': personal_writeup,
        'job_post': job_post,
        'resume': resume
    }

    crew = ResumeCrew().crew().kickoff(inputs)
    return crew


def resume_save(name, linkdin_url, github_url, personal_writeup, job_post, resume):
    task_ref = db.collection('tasks').document(name)
    task_ref.update({'status': 'in progress'})

    result = resume_crew(linkdin_url, github_url, personal_writeup, job_post, resume)

    task_ref.update({
        'status': 'completed',
        'result': result
    })
