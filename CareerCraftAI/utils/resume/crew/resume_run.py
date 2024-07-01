from utils.resume.crew.resume_agents import ResumeCrew

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
