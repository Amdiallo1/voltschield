import uuid
import json
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
QUEUE_DIR = "task_queue"
os.makedirs(QUEUE_DIR, exist_ok=True)

class CustomerRequest(BaseModel):
    customer_name: str
    email: str
    issue_description: str

@app.post("/run-crew")
async def run_crew_endpoint(request: CustomerRequest):
    # Setup the Agent
    analyst = Agent(
        role="Expert Electrician",
        goal="Provide safety and scope analysis",
        backstory="Expert with 30 years experience",
        llm="gpt-4o-mini"
    )

    # Setup the Task
    task = Task(
        description=f"Issue from {request.customer_name}: {request.issue_description}",
        expected_output="Safety hazards, project scale, and next steps.",
        agent=analyst
    )

    # Execute
    crew = Crew(agents=[analyst], tasks=[task])
    
    # Run the crew
    result = await crew.kickoff_async()
    
    # Return result to user
    return {"status": "success", "analysis": str(result)}

