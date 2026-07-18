Set-Content -Path .\main.py -Value @'
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew

app = FastAPI(title="VoltShield API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class CustomerRequest(BaseModel):
    customer_name: str
    email: str
    issue_description: str

@app.get("/")
def read_root():
    return {"status": "online"}

@app.post("/run-crew")
async def run_crew_endpoint(request: CustomerRequest):
    try:
        # Define the agent
        analyst = Agent(
            role="Senior Electrical Triage Expert",
            goal="Analyze electrical issues for safety and scope.",
            backstory="Expert electrician with decades of experience.",
            llm="gpt-4o-mini"
        )
        
        # Define the task
        task = Task(
            description=f"Issue from {request.customer_name}: {request.issue_description}",
            expected_output="Safety hazards, project scale, and next steps.",
            agent=analyst
        )
        
        # Assemble and execute
        crew = Crew(agents=[analyst], tasks=[task])
        
        # Native async kickoff
        result = await crew.akickoff()
        
        return {"status": "success", "message": str(result)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
'@
