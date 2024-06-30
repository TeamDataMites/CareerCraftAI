from utils.resume.crew.resume_agents import ResumeCrew

def resume_crew(linkdin_url, github_url, user_information, job_posting_url, resume):
    inputs = {
        'linkdin_url': linkdin_url,
        'github_url': github_url,
        'user_information': user_information,
        'job_posting_url': job_posting_url,
        'resume': resume
    }

    crew = ResumeCrew().crew().kickoff(inputs)
    return crew


if __name__ == "__main__":
    linkdin_url = "https://www.linkedin.com/in/visith-kumarapperuma-283851200"
    github_url = "https://github.com/visith1577"
    user_infromation = """
                    """
    job_posting_url=""
    resume=""
    
    resume_crew(linkdin_url, github_url, user_infromation, job_posting_url, resume)
