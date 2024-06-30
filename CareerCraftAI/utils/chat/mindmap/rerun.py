from agent import mindmap_agent


if __name__ == '__main__':
    desc = """
    Role description  The Principal Data Scientist will use both management experience and data science expertise to lead teams of data scientists across multiple analytics projects. 
    This person will be an integral part of conceptualizing, scoping and delivering complex analytics projects. 
    They will oversee the development, testing and maintenance of analytical models which mimic business decisions. 
    This person will work closely with the Octave leadership and business units in delivering impact through analytics. 
    Additionally, this person will be responsible for continuously identifying opportunities to improve the ways of working and structuring within the analytics center of excellence.  
    Key responsibilities 
    • Define and manage analytics strategy across multiple businesses 
    • Provides analytical expertise in the process of model development, refining and implementation in a variety of analytics problems spread across a variety of domains 
    • Oversees large teams of associate and mid level data scientists, de-bottlenecking issues related to project execution 
    • Work closely with translators and business teams to develop and implement analytics solutions 
    • Collaborate with data engineers & architects to implement and deploy scalable solutions 
    • Communicate results to diverse technical and non technical audiences 
    • Actively drive a culture of knowledge building and sharing within the team. 
    Encourage continuous innovation and out of the box thinking.  
    Desired Skills / Competencies  Education + Technical skills / experience 
    • Master’s degree in Computer Science, Statistics, Math, Operations Research, Economics or a related field 
    • Experience in programming in at least 2 languages 
    • Sound theoretical and practical knowledge of working with advanced statistical algorithms, including machine learning techniques 
    • At least 10 years of experience of working in analytics 
    • At least 4 years of experience managing analytics teams. 
    Experience in developing teams from scratch a plus. 
    • Strong business understanding. Worked in developing analytics solutions in 3-4 domains  Managerial Skills 
    • Ability to lead teams in agile environments, with multiple stakeholders involved 
    • Ability to effectively communicate complex technical content to non-technical audience 
    • Successful track record of structuring and leading complex analytics projects  Mindset & Behavior 
    • Proactive and passionate about resolving pain points through great design 
    • Sees value in iterative approach to model development 
    • Strong sense of ownership and ability to build consensus 
    • Believes in culture of transparency and trust"""

    meg = mindmap_agent(
        desc
    )

    print(meg)