import os
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crewai.llm import LLM

# 1. Initialize FastAPI
app = FastAPI()

# 2. Define Request Structure
class Booking(BaseModel):
    fullName: str
    email: str
    phone: str
    serviceType: str
    inspectionDate: str
    notes: str

# 3. Configure AI Model
# Ensure OPENAI_API_KEY is set in your Render Environment Variables
api_key = os.getenv("OPENAI_API_KEY", "")
custom_llm = LLM(model="gpt-4o-mini", api_key=api_key)

@app.get("/")
def read_root():
    return {"status": "online", "message": "VoltShield API is active"}

# 4. Booking Endpoint with Error Handling
@app.post("/submit-booking")
async def submit_booking(booking: Booking):
    # SMTP Configuration (Use Environment Variables for security!)
    smtp_server = "smtp.yandex.com"
    smtp_port = 465
    sender_email = os.getenv("EMAIL_USER")  # Set these in Render Dashboard
    password = os.getenv("EMAIL_PASS")      # Set these in Render Dashboard

    try:
        # Construct Email
        msg = EmailMessage()
        msg["Subject"] = f"New Booking: {booking.serviceType}"
        msg["From"] = sender_email
        msg["To"] = sender_email
        msg.set_content(
            f"New Booking Details:\n\n"
            f"Name: {booking.fullName}\n"
            f"Email: {booking.email}\n"
            f"Phone: {booking.phone}\n"
            f"Service: {booking.serviceType}\n"
            f"Date: {booking.inspectionDate}\n"
            f"Notes: {booking.notes}"
        )

        # Send with Timeout
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        
        return {"status": "success", "message": "Booking received and email sent."}

    except Exception as e:
        print(f"CRITICAL ERROR: {e}") # This prints to Render Logs
        raise HTTPException(status_code=500, detail=str(e))
