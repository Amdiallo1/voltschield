import os
import resend
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 🤖 CrewAI Imports
from crewai import Agent, Task, Crew, Process

# Initialize FastAPI
app = FastAPI(title="Voltshield Electrical Engine")

# Allow GitHub Pages to connect seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://amdiallo1.github.io"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resend.api_key = os.getenv("RESEND_API_KEY")
# CrewAI automatically uses the environment variable named: OPENAI_API_KEY

class Booking(BaseModel):
    fullName: str
    email: str
    phone: str
    serviceType: str
    inspectionDate: str
    notes: str

def send_booking_email(booking: Booking, ai_report: str):
    html_content = f"""
    <h3>⚡ New Booking Processed by CrewAI Agents</h3>
    <p><strong>Customer:</strong> {booking.fullName}</p>
    <p><strong>Email:</strong> {booking.email} | <strong>Phone:</strong> {booking.phone}</p>
    <p><strong>Requested Service:</strong> {booking.serviceType}</p>
    <p><strong>Target Date:</strong> {booking.inspectionDate}</p>
    <p><strong>Client Input:</strong> "{booking.notes}"</p>
    
    <hr style="border: 1px solid #cbd5e1;">
    <h3 style="color: #f59e0b;">🤖 Agent Intake & Assessment Report:</h3>
    <div style="background-color: #f8fafc; padding: 15px; border-radius: 6px; font-family: monospace; white-space: pre-wrap;">
    {ai_report}
    </div>
    """
    return resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": "amdiallo1@yandex.com", 
        "subject": f"⚡ AI Intake: {booking.serviceType} - {booking.fullName}",
        "html": html_content
    })

@app.post("/run-crew")
def run_crew(request: CustomerRequest):  # 1. Matches your new route path & data schema, 'async' removed!
    try:
        # 2. Define the Electrical Expert Agent inside a safe synchronous thread
        analyst = Agent(
            role="Senior Electrical Triage Expert",
            goal="Analyze customer requests to determine project scope, required materials, and safety priorities.",
            backstory="You are an expert electrician with decades of field experience. You look at client descriptions, identify core hazards (like exposed wiring or overload signs), and outline technical requirements.",
            verbose=False,
            memory=False
        )
        
        # 3. Define the specific task for your agent
        analysis_task = Task(
            description=(
                f"Analyze the following problem submitted by {request.customer_name} ({request.email}):\n"
                f"\"{request.issue_description}\"\n\n"
                "Identify potential hazards, project scale, and required safety steps."
            ),
            expected_output="A detailed summary outlining safety concerns, estimated project type, and material recommendations.",
            agent=analyst
        )
        
        # 4. Form the Crew and kickoff synchronously
        crew = Crew(
            agents=[analyst],
            tasks=[analysis_task],
            verbose=False
        )
        
        result = crew.kickoff()
        
        # 5. Return the response string cleanly to your client
        return {"status": "success", "message": str(result)}
        
    except Exception as e:
        return {"status": "error", "message": f"AI Crew failed to process your request: {str(e)}"}
          
        )

        # 2. Define the Communications Strategist Agent
        strategist = Agent(
            role="Voltshield Customer Liaison",
            goal="Draft a highly professional operational response blueprint and next steps roadmap.",
            backstory="You bridge the gap between heavy technical jargon and elite customer care. You summarize operational steps and make sure the customer feels valued and safe.",
            verbose=False,
            memory=False
        )

        # 3. Create the tasks passing the booking data directly into the prompts
        task_analysis = Task(
            description=f"""Analyze the following customer booking data:
            - Service Category: {booking.serviceType}
            - Customer Notes: "{booking.notes}"
            Identify potential hazards, specific tools or parts that will likely be needed, and a ballpark complexity score (Low/Medium/High).""",
            expected_output="A structured technical breakdown listing hazards, preparation steps, and necessary tools.",
            agent=analyst
        )

        task_roadmap = Task(
            description="Review the technical breakdown. Generate a brief internal dispatch summary and a 3-step action item plan for the team to reference before contacting the client.",
            expected_output="A clean dashboard summary with clear, immediate actionable next steps.",
            agent=strategist
        )

        # 4. Fire up the crew sequentially
        voltshield_crew = Crew(
            agents=[analyst, strategist],
            tasks=[task_analysis, task_roadmap],
            process=Process.sequential
        )

        # Kickoff the agent workflow using your OpenAI Account
        crew_result = voltshield_crew.kickoff()
        ai_report = str(crew_result)

        # 5. Send out the email alert containing the AI's deep insights
        send_booking_email(booking, ai_report=ai_report)
        
        return {"status": "success", "message": "Booking received and analyzed by your crew!"}
        
    except Exception as e:
        print(f"DEBUG: Crew execution or mail delivery failed: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
     
