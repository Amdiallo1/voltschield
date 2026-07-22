import os
import asyncio
import traceback
import resend
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew

# 1. Validate and set environment variables
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is missing.")
os.environ["OPENAI_API_KEY"] = openai_key

resend.api_key = os.getenv("RESEND_API_KEY")

# 2. Initialize FastAPI app
app = FastAPI(title="VoltShield API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Request Schema
class CustomerRequest(BaseModel):
    customer_name: str
    email: str
    issue_description: str

# 4. CrewAI Setup
inspector_agent = Agent(
    role="Electrical Safety Inspector",
    goal="Analyze electrical issues for compliance, safety risks, and necessary remediation steps.",
    backstory="Expert electrical engineer specializing in commercial and residential compliance codes.",
    verbose=True
)

inspection_task = Task(
    description=(
        "Analyze the following electrical issue reported by {customer_name} "
        "(Email: {email}):\n\n'{issue_description}'\n\n"
        "Provide a structured safety analysis, risk level, and compliance recommendations."
    ),
    expected_output="A professional safety analysis and compliance report.",
    agent=inspector_agent
)

voltshield_crew = Crew(
    agents=[inspector_agent],
    tasks=[inspection_task],
    verbose=True
)

# 5. Endpoints
@app.get("/")
def read_root():
    return {"status": "online", "service": "VoltShield API"}

@app.post("/run-crew")
async def run_crew(request: CustomerRequest):
    try:
        def execute_crew():
            return voltshield_crew.kickoff(inputs={
                "customer_name": request.customer_name,
                "email": request.email,
                "issue_description": request.issue_description
            })

        result = await asyncio.to_thread(execute_crew)
        return {"status": "success", "result": str(result)}

    except Exception as e:
        error_detail = {
            "error_type": type(e).__name__,
            "message": str(e),
            "traceback": traceback.format_exc()
        }
        print("CRITICAL ERROR:", error_detail)
        raise HTTPException(status_code=500, detail=error_detail)
