from utils.resume.crew.resume_agents import ResumeCrew

def resume_crew(linkdin_id, linkdin_url, github_url, user_information, job_posting_url, resume):
    inputs = {
        'linkdin_id': linkdin_id,
        'linkdin_url': linkdin_url,
        'github_url': github_url,
        'user_information': user_information,
        'job_posting_url': job_posting_url,
        'resume': resume
    }

    crew = ResumeCrew().crew().kickoff(inputs)
    return crew


if __name__ == "__main__":
    linkdin_id = "1234"
    linkdin_url = "https://www.linkedin.com/in/username"
    github_url = ""
    user_infromation = """
                    """
    job_posting_url=""
    resume=""
    
    resume_crew(linkdin_id, linkdin_url, github_url, user_infromation, job_posting_url, resume)
