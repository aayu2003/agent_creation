from crewai import Agent 
from tools import url_extractor_tool
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

llm=ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    verbose=True,
    temperature=0.5,
    api_key="AIzaSyCttE7CHlvxpD3o4bNMHi7Sj52IHPbfaTU"

)

# creating a task decomposer 

plan_agent=Agent(
    role='divides the {Query} into smaller subtasks',
    goal='optimal subtask finder for {Query}',
    verbose=True,
    memory=True,
    backstory=('expert in finding the optimal subtasks that should be done in order to achieve the goal'),
    tools=[url_extractor_tool],
    llm=llm,
    allow_delegation=True
)

# task executer

tool_agent=Agent(
    role='market analyst ',
    goal='research for {Query} and give a small analysis',
    verbose=True,
    memory=True,
    backstory=('an expert market analyst that go through many news papers and reports and analyze the makrket trend . moreover predicting the further market trends.'),
    tools=[url_extractor_tool],
    llm=llm,
    allow_delegation=False
)