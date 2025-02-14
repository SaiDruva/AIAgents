import os
import json
import requests
import speech_recognition as sr
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Set your OpenAI API key (either via environment variable or directly)
openai_api_key = os.getenv("OPENAI_API_KEY") 

def capture_voice():
    """
    Agent 1: Captures voice input from the microphone and returns the transcribed text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak now!")
        audio = recognizer.listen(source)
    try:
        transcript = recognizer.recognize_google(audio)
        print("Transcript:", transcript)
        return transcript
    except Exception as e:
        print("Error capturing voice:", e)
        return None

def generate_jira_details(transcript: str):
    """
    Agent 2: Uses LangChain with OpenAI to extract JIRA ticket details from the voice transcript.
    Returns a dictionary with keys "title" and "description".
    """
    prompt_template = PromptTemplate(
        input_variables=["transcript"],
        template="""
You are an assistant that extracts JIRA ticket details from a voice transcription.
The user said: "{transcript}"
Please provide a JSON object with two keys:
- "title": a concise summary of the issue.
- "description": a detailed explanation of the issue.
Return only the JSON object.
"""
    )
    
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(transcript=transcript)
    print("LLM output:", response)
    
    try:
        details = json.loads(response)
        return details
    except json.JSONDecodeError as e:
        print("Error parsing JSON from LLM output:", e)
        return None

def create_jira_ticket(details: dict):
    """
    Agent 3: Uses the JIRA REST API to create a ticket with the provided details.
    The description is formatted using the Atlassian Document Format (ADF).
    Replace the placeholder values with your actual JIRA configuration.
    """
    # Update these with your actual JIRA configuration.
    jira_domain = ""
    email = ""
    token = ""
    project_key = ""
    
    # Wrap the description text in Atlassian Document Format (ADF)
    description_text = details.get("description", "No Description Provided")
    description_adf = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": description_text
                    }
                ]
            }
        ]
    }
    
    url = f"{jira_domain}/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": details.get("title", "No Title Provided"),
            "description": description_adf,
            "issuetype": {"name": "Task"}
        }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            url,
            data=json.dumps(payload),
            headers=headers,
            auth=(email, token)
        )
        if response.status_code == 201:
            print("JIRA ticket created successfully!")
            return response.json()
        else:
            print("Failed to create ticket:", response.status_code, response.text)
            return None
    except Exception as e:
        print("Error creating JIRA ticket:", e)
        return None

def voice_to_jira_workflow():
    """
    Orchestrates the three-agent workflow:
      1. Capture voice and transcribe.
      2. Generate JIRA ticket details using LangChain and OpenAI.
      3. Create the JIRA ticket.
    """
    transcript = capture_voice()
    if not transcript:
        print("No transcript captured. Aborting workflow.")
        return
    
    details = generate_jira_details(transcript)
    if not details:
        print("Failed to generate JIRA details. Aborting workflow.")
        return
    
    ticket = create_jira_ticket(details)
    if ticket:
        print("Workflow completed successfully. Ticket details:")
        print(ticket)
    else:
        print("Workflow failed at the ticket creation step.")

if __name__ == "__main__":
    voice_to_jira_workflow()
