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
async def run_crew(request: CustomerRequest):
    try:
        # ❌ This line crashes because it runs synchronously inside FastAPI's async loop
        result = voltshield_crew.kickoff(inputs={
            "customer_name": request.customer_name,
            "email": request.email,
            "issue_description": request.issue_description
        })
        return {"status": "success", "message": result}
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
     
