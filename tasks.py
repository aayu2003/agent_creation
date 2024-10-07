from crewai import Task
from tools import url_extractor_tool
from agent import plan_agent,tool_agent

# task decomposition 

plan_task=Task(
    description=(
        "find the relavent information for {Query} ."
        "divide {Query} into smaller and most optimal tasks ."
        ),
    expected_output='a list of the smaller optimally divided task for successfully completing {Query}',
    tools=[url_extractor_tool],
    agent=plan_agent
)

#execution task

tool_agent_task=Task(
    description=(
        "execute the subtasks that we got from {Query} ."
        "get detailed analysis about the market trends"
        ),
    expected_output='a comprehensive paragraph on the analysis done by successfully executing the subtasks that have been optimally found from {Query} and make the analysis report',
    tools=[url_extractor_tool],
    agent=tool_agent,
    async_execution=True,
    output_file='aayush.txt'
)