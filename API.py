from flask import Flask, request, jsonify , render_template
from crewai import Agent
from tools import url_extractor_tool
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool
from crewai_tools import SeleniumScrapingTool
from crewai import Crew,Process
from crewai import Task
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "hackathon-8d0fa",
  "private_key_id": "a6121cceafe54e16ffa2d1674beb3b5a7232c611",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQC2wC5wfRuD7E4d\nH1Iq7H1TBIJmKc8peVy+aN9BHxqs811hgBoL11xoKkyCj6M1B13HeM93XksBoiWG\nlSKSshhJ0VYEs3G0JCFxlFiaEi0ronD7H8wgwqdFp5A3DjVd/hCNBP/5tRbJ9fE+\nFEFYTl40O0EYktcyV8iT2nmeeu9LG9Ha3u8rPLoI5e8ajCRjliWwtZ552nPMyorC\nO+XeqbxlU+pJ2Os4XUhC7Y58AbMPVrWHIHXxeiZZOAayXcJGSC0LlLoHZlpikV0B\n7HrZxExRabrRW+WdOzUxZUM2eq0mKfQHfTNGX0cbqKqT/CGr9ZqY2O7KrPwJ5MQK\nrnQtUFw1AgMBAAECgf8L55ce2ulg41aryzjh3jqmFzQrKELHaVUwXXdazivnJ1y5\nMfHp046TWKaFJhJ0Hh1QnWht7UWbN4Pf7anxAordy66aGEOTrT9TTG0t2GqvdIOc\nULm3pNhex89ZbG3gXsMeqNLWxDjshaf8thjW649GfWh8ZgVTZ9z74s6Q5jT7p+yn\n/NRPaKxjIdzHuKPAXlnj/hTJEVEiAlFhWflc0Icl1xQPpwKfCzMGrpngbFSLtBr9\nGg18dz/HYJpla73xpM1cet1lo+ktFwwIn+JpKHb95Dm4Dgydhc55dyTVm6J0/2dQ\nYffHpqIrVXQ2VwosbgYJnlPcaqGzWe1dV5LX10sCgYEA77CCv8UymSEDrEIH9qwU\nvd2mZCw0bqHD1WYPVeFEv33znc6okwB9Mv5M6U5xwiS3tD41v8H/6Sw5+a24JzO7\nkFndP2pHmGAlVA/mXaUbGkYGlHEhUdYpccCqdxjbV4u/Z1k53xHD9IzEUgdbQ6qr\neUkuySug0ca7fmkTCl+eZ4MCgYEAwy/GDtWD1XmKcyVXW0k2sCZHMfkw3YTWQFCL\nWwoe4X0Kp2SvBeh8WNLdc4Pgvl/xkRJD7NIvSiA28j6Fr6jYv9WRscd7jjJEfVbI\nnOOkVTgIrQhl3etwbFg80XJAF6dJBWnBfCaXr55LM7jguTm+TLRtAdEHT76uwor2\nNb80J+cCgYEArxreikcATgpmaoPa2YShqouxMWFx9JjNPqtO7MijttnHDjSZxrsG\nvCg3/AHI7bJxWoZQMgUCdlBPEm6tKEaM8koUbm2wXEtxOdZbz3H9ONaLnAqB8w1o\nPagpYNSR+YUokdIHi0WpSJFGIz8ol2ip2PNz8Jek51wuQY110ZBFYw0CgYAILaZE\n1NlzRmZwsK3aW1T5SIFPLLvJbFl11GoiZGgq1oxtuyBCRR2As0UoI+x0zZxXkcZa\n0+u7VWI4ADqlw5NhZld2dX9N0/lerxY0zK0EDRb/+QwbolPRlljmBb19wDqlCWtc\nAln0t9M61ZJE8JByslSm8NU3mCvGZwAt/Fb5HQKBgEya2gQzBxp9tgNWHCTkaS6u\ntKeORO9F3esnoQEpRf+DVRcfanx9Cr25hb++s+AqEwu80SXpI+cZUPHzIMqGt8Co\nisiXr7G7ZT2pYxhYUpO+QiLDh6BprBin0fvNgMUnA8tOdQBOCgA85U8pthzH2a91\n80hdxv0vaVnNH9goTowx\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-pbyfu@hackathon-8d0fa.iam.gserviceaccount.com",
  "client_id": "113542427700727811206",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-pbyfu%40hackathon-8d0fa.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})  # Update with your key path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://hackathon-8d0fa-default-rtdb.firebaseio.com/'  # Update with your database URL
})

app = Flask(__name__)
os.environ["SERPER_API_KEY"] = "a7bd701137f2a9b615ef9f7c91389db06713e412"

# Initialize the SerperDevTool
url_extractor_tool = SerperDevTool(verbose=True)
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash',
                            verbose=True,
                            temperature=0.5,
                            goggle_api_key="AIzaSyCttE7CHlvxpD3o4bNMHi7Sj52IHPbfaTU")    

chat_sessions = {'Query':None , "Subtask_old":None , "response":None , "Additional_information":None }

def subtask_agent(Query):
    plan_agent=Agent(
    role='divides the {Query} into smaller subtasks',
    goal='optimal subtask finder for {Query}',
    verbose=True,
    memory=True,
    backstory=('expert in finding the optimal subtasks that should be done in order to achieve the goal'),
    tools=[url_extractor_tool],
    llm=llm,
    allow_delegation=True)

    plan_task=Task(
        description=(
            "find the relavent information for {Query} ."
            "divide {Query} into smaller and most optimal tasks ."
            ),
        expected_output='a list response of the optimally divided task for successfully completing {Query} , these subtasks must be descriptive',
        tools=[url_extractor_tool],
        agent=plan_agent
        
    )

    crew=Crew(
        agents=[plan_agent],
        tasks=[plan_task],
        process=Process.sequential,
    
    )

    result=crew.kickoff(inputs={'Query':Query})
    return result

def user_subset(subtasks,Query):
    plan_agent=Agent(
        role='{subtasks} differentiator ',
        goal='differentiate from a set of {subtasks} which subtasks requires more clarification from the user',
        verbose=True,
        memory=True,
        backstory=('expert in differentiating the {subtasks} so that we can get more clarity on by user input in order to achieve the goal'),
        tools=[url_extractor_tool],
        llm=llm,
        allow_delegation=True
    )

    plan_task=Task(
        description=("differentiate the {subtasks} in such a way that the response should contain the subset of the {subtasks} in which we require more clarity from the user to get the best output also the subset can be empty too which means there is no such subtask which require the user input ."),
        expected_output='a subset of {subtasks} that requires the user input for more clarity about the {Query} given',
        tools=[url_extractor_tool],
        agent=plan_agent
        
        
    )

    crew=Crew(
        agents=[plan_agent],
        tasks=[plan_task],
        process=Process.sequential,
    
    )

    result1=crew.kickoff(inputs={'Query':Query,'subtasks':subtasks})
    return result1

def task_executor(subtasks,additional_information):
    plan_agent=Agent(
        role='{subtasks} subtask executer ',
        goal='successful find the answer to the  {subtasks} with additional information as {additional_information}',
        verbose=True,
        memory=True,
        backstory=('expert in finding the answers and cmplete the subtasks that should be done in order to achieve the goal'),
        tools=[url_extractor_tool],
        llm=llm,
        allow_delegation=True
    )

    plan_task=Task(
        description=(
            "find the relavent information for {subtasks} and always consider the additional information as {additional_information} in order to produce best output ."
            "make a report of 3 paragraph breifly describing the solutions and answers of {subtasks} with additional information {additional_information} in such a way that all the aspect is covered acurately ."
            ),
        expected_output='a short comprehensive paragraph description , solution and answers to the {subtasks} with additional information as {additional_information}',
        tools=[url_extractor_tool],
        agent=plan_agent
        
    )

    crew=Crew(
        agents=[plan_agent],
        tasks=[plan_task],
        process=Process.sequential,
    
    )

    result2=crew.kickoff(inputs={'subtasks':subtasks , 'additional_information':additional_information})
    return result2

def response_refiner(new_response,Query):
    refining_agent=Agent(
        role='{response} refiner ',
        goal='successful finds weather the {response} matches with the {Query} and makes a response which is in {response} and matches the {Query}',
        verbose=True,
        memory=True,
        backstory=('expert in giving the responses which answers to the {Query} in the best way possible from {response}.'),
        tools=[url_extractor_tool],
        llm=llm,
        allow_delegation=True
    )

    plan_task=Task(
        description="find weather the {response} fully answer {Query} or not . if {response} contains irrelavant information also which is extra to {Query} removing the extra part .Giving the fresh response which is highly similar to the {Query}",
        expected_output='a short comprehensive paragraph description of a relavant response which is taken from {response} and it should be precicely inswering the {Query}',
        tools=[url_extractor_tool],
        agent=refining_agent
        
    )

    crew=Crew(
        agents=[refining_agent],
        tasks=[plan_task],
        process=Process.sequential,
    
    )

    result3=crew.kickoff(inputs={'Query':Query , 'response':new_response})

    return result3



@app.route('/')
def index():
    return render_template('a.html')

@app.route('/chat', methods=['GET'])
def chat():
    try:
        Query = request.args.get('query')  # Extract 'query' from the URL
        additional_information = request.args.get('additional_info')
        user_id=request.args.get('user_id')  # Extract 'additional_info' from the URL
    except:
        return jsonify({'response':'None'})

    ref=db.reference('/chat_session')
    all=ref.get()
    print(all)
    if user_id in all.keys():
        url='/chat_session/'+user_id
        new_ref=db.reference(url)
        chat_sessions=new_ref.get()
        chat_sessions['Query']=Query
        #made the subtasks 
        subtasks=subtask_agent(Query)
        #dividing the subtasks we need from user
        chat_sessions['Subtask_old']=subtasks
        
        user_sub=user_subset(subtasks,Query)
        if not additional_information:
            
            
            return jsonify({'response':user_sub,
                            'additional_information':0})


        else:
            chat_sessions['Additional_information']=additional_information
            response=task_executor(chat_sessions['Subtask_old'],additional_information)
            chat_sessions['response']=response
        # refining the response 
        response_new=response_refiner(chat_sessions['response'],chat_sessions['Query'])
        return jsonify({
            'response':response_new,
            'additional_information':1
        }) , 200

    else:
        new_ref=ref.child(user_id)

        chat_sessions={'Query':None , "Subtask_old":None , "response":None , "Additional_information":None }

        chat_sessions['Query']=Query
        #made the subtasks 
        subtasks=subtask_agent(Query)
        #dividing the subtasks we need from user
        chat_sessions['Subtask_old']=subtasks
        
        user_sub=user_subset(subtasks,Query)
        if not additional_information:
            new_ref.set(chat_sessions)
            
            return jsonify({'response':user_sub,
                            'additional_information':0})


        else:
            chat_sessions['Additional_information']=additional_information
            response=task_executor(chat_sessions['Subtask_old'],additional_information)
            chat_sessions['response']=response
        # refining the response 
        response_new=response_refiner(chat_sessions['response'],chat_sessions['Query'])
        return jsonify({
            'response':response_new,
            'additional_information':1
        }) , 200


if __name__ == '__main__':
    app.run(debug=True)