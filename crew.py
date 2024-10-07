from crewai import Crew,Process
from agent import plan_agent , tool_agent
from tasks import plan_task , tool_agent_task

crew=Crew(
    agents=[plan_agent,tool_agent],
    tasks=[plan_task , tool_agent_task],
    process=Process.sequential,
    memory=True,
    cache=True,
    max_rpm=100,
    share_crew=True
)

# start process with feedback 

result=crew.kickoff(inputs={'Query':'why tata sales are getting stronger day by day'})
print(result)
