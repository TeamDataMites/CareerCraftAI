from utils.resume.crew.resume_agents import ResumeCrew

def resume_crew(linkdin_url, github_url, user_information, job_post, resume):
    inputs = {
        'linkdin_url': linkdin_url,
        'github_url': github_url,
        'personal_writeup': user_information,
        'job_post': job_post,
        'resume': resume
    }

    crew = ResumeCrew().crew().kickoff(inputs)
    return crew


if __name__ == "__main__":
    linkdin_url = "https://www.linkedin.com/in/visith-kumarapperuma-283851200"
    github_url = "https://github.com/visith1577"
    personal_writeup = """
I am Visith kumarapperuma. I am a undergraduate of UCSC. I am a machine learning engineer. I have research interests in NLP and computer vision.
I have experience in working and managing teams.
                    """
    job_post="Company Description  IFS is a billion-dollar revenue company with 6000+ employees on all continents. We deliver award-winning enterprise software solutions through the use of embedded digital innovation and a single cloud-based platform to help businesses be their best when it really matters–at the Moment of Service™.  At IFS, we're flexible, we're innovative, and we're focused not only on how we can engage with our customers, but on how we can make a real change and have a worldwide impact. We help solve some of society's greatest challenges, fostering a better future through our agility, collaboration, and trust.  We celebrate diversity and accept that there are so many different perspectives in this world. As a truly international company serving people from around the globe, we realize that our success is tantamount to the respect we have for those different points of view.  By joining our team, you will have the opportunity to be part of a global, diverse environment; you will be joining a winning team with a commitment to sustainability; and a company where we get things done so that you can make a positive impact on the world.  We're looking for innovative and original thinkers to work in an environment where you can #MakeYourMoment so that we can help others make theirs.  If you want to change the status quo, we'll help you make your moment. Join Team Purple. Join IFS  Job Description  This role is all about hands-on technical prowess. You'll be individual contributor, working in a team with autonomy, accountability, and technical brilliance. Your mission includes:  · Delivering high-value AI/ML prospects within our product offerings.  · Demonstrating curiosity in the latest and greatest tech trends.  · Framing problems and solutions with proofs of concept to the grand finale of implementation, you'll ensure scalability and top-tier performance.  · Collaborating with Data Engineers, ML Engineers, Software Engineers, Solution Architects, and Product/Program Managers. Collectively, you will define, create, deploy, monitor, and document ML models  Qualifications  · 1 - 5 years of data science expertise, backed by proven ability with successful projects.  · Skilled in bringing AI/ML solutions to life from start to finish, including scoping, design, development, testing, deployment, and vigilant monitoring.  · Expertise creating and delivering Cloud ML solutions at scale using Docker and Kubernetes.  · Understanding of advanced statistical modeling and analysis  . Expertise in Python and the tools and libraries that make ML magic happen.  · Familiarity with ML experiment tracking and collaboration tools, such as Mlflow and Weights & Biases.  · A solid in software engineering and DevOps practices, MLOps deployment, and infrastructure.  · Curiosity and understanding of generative AI frameworks and SDKs, like RAG, Langchain, Semantic Kernel, and tools such as MS tooling, Co-Pilot Studio, ML Studio, Prompt flow, Kedro, etc.  · Worked with pipeline orchestration tools, such as Airflow, Kubeflow, and Argo.  · Good communication skills, combining subject matter expertise with a flair for statistics.  · A results-driven attitude, a passion for innovation, and a self-starting, proactive nature. You're organized, capable of juggling multiple tasks, and your creativity knows no bounds. You're a strategic thinker, always on the hunt for the next big thing.  Additional Information  Interviews and selections are made continuously. If you are interested, apply as soon as possible.  As a step in our recruitment process, all final candidates will undergo a background check, to get us an understanding of our future employees.  We respectfully decline all offers of recruitment and/or advertising assistance"
    resume="""
## Visith kumarapperuma

## Undergraduate at University of

## Colombo School of Computing

# Personal details

```
Visith kumarapperuma
```
```
visithkumarapperuma@gmail.
com
```
### 0755774023

```
31/213 Balika Niwasa rd,
Rukmale Pannipitiya
```
```
May 23 , 2001
```
```
linkedin.com/in/visith-
kumarapperuma- 283851200
```
```
github.com/visith
```
```
kaggle.com/visithk
```
# Skills

Python programming

Backend development

Go programming

LLm development

Selenium

Learning New Skills

Problem Solving

# Profile

```
Self learned developer currently an Undergraduate at University of Colombo
School of Computing in Computer science. I am an ambitious and forward thinking
developer who seeks broaden Knowledge in LLm's and Computer vision. I am
eager to get hands on experience in solving real world problems to learn and
collaborate with like minded individuals.
```
# Education

```
G.C.E Ordinary Level | English Medium 2017
I - Gate College, Thalawathugoda
8 - A and 1 - B
```
```
G.C.E Advanced Level | Physical Science |
English medium
```
### 2018 - 2021

```
Ananda College, Colombo - 10
( Combined math - A | Chemistry - B | Physics - A )
```
```
B.Sc. Computer Science Jun 2022 - Present
University of Colombo School of Computing
```
# Technical Skills

```
Programming - Python, Go, Rust, C++
```
```
Web Scraping with Beautiful soup
```
```
SQL, No SQL databases
```
```
Vector databases - Waeviate, Chroma
```
```
Llm development with Chatgpt, Llama & Gemma
```
```
Langchain
```
```
Tensorflow & PyTorch for deep learning
```
```
Data visualization with Python
```
```
Flutter app development
```
```
Java, Node.js, Go, Fast API backend
```
```
computer vision using openCV and DL models
```
```
Using Machine learning for predictions and data analysis
```
# Certificates

```
Deep learning Specialization by Andrew Ng Dec 2020
Certificate
```
```
Deeplearning.Ai Tensorflow : Advanced
Techniques
```
### 2021


# Languages

Sinhala

English

# Interests

```
Machine learning
```
```
Computer vision
```
```
NLP
```
```
Devops
```
```
Cloud computing
```
# Qualities

```
Curiosity and Eager to learn new
technologies
```
```
Flexible and willing to Adapt to new
methodologies and technologies.
```
```
Attention to detail when problem
solving
```
```
certificate
```
```
DeepLearning.Ai Tensorflow Developer
specialisation
```
### 2021

```
Natural Language processing Specialisation 2021
certificate
```
```
Google Data Analytics
certificate
```
```
Deep Learning.Ai short course series on LLm
developement
```
```
Present
```
```
DeepLearning.Ai free course series on developing LLm's, MLops, and RAG model
with vector databases
```
```
PyTorch: Deep learning and Artificial
Intelligence | Udemy
```
# Projects

```
UtilitySaga
utility management system, built to track electricity and water consumption via IoT
devices and for relevant authorities to maintain faster and organised
communication with the users
Tech stack - Java, HTML, CSS, Javascript, OpenAi api
```
```
EcoBubble
Project as submission for SLIoT challenge. Monitor plants within a green house
using Arduino and computer vision. Computer vision models to detect plant
diseases and abnormalities & LLm for automated report generation.
```
```
PetsPawtal - ongoing
Pet feeder application uses IoT to monitor and automate feeding pets on time.
Built with Flutter
```
```
Law LLm model
LLm chat bot to assist in providing law advice. Ongoing project that uses OpenAi
api, Weaviate and Langchain.
```
# Competitions

```
Fresh-Hack 3.0 organised by UCSC - placed 21st
Open-Hack Organised by IIT - placed 20th
Datathon SLIIT 2023 - Participation
Datathon SLIIT 2024 - Participation
Mini Hakathon 2023 Organised by Stat Circle and Octave - Finalist and top 10
SLIoT organised by UoM CSE - participation
Kaggle competitions:
```
- Google - Ai assistants for data tasks with Gemma

```
Joined - Ongoing
Codesprint 2024 - organised by IIT
IntelliHack 2024 - Organised by IEEE CS student branch of UCSC
"""
    
item = resume_crew(linkdin_url, github_url, personal_writeup, job_post, resume)

print(item)
