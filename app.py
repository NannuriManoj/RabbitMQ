import os
from datetime import datetime
import logging
from smtplib import SMTP, SMTPException
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import PlainTextResponse
from celery import Celery
from dotenv import load_dotenv

# Load .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Environment variables
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
BROKER_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "rpc://")

# Logging
logging.basicConfig(filename="messaging_system.log", level=logging.INFO)

app = FastAPI()
celery = Celery("tasks", broker=BROKER_URL, backend=RESULT_BACKEND)

@celery.task
def send_email_task(to_email: str):
    try:
        with SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.sendmail(GMAIL_USER, to_email, "Subject: Test\n\nEmail from FastAPI + Celery")
            logging.info(f"Email sent to {to_email}")
    except SMTPException as e:
        logging.error(f"Failed to send email to {to_email}: {str(e)}")


@app.get("/")
async def index(sendmail: str = Query(None), talktome: str = Query(None)):
    if sendmail:
        try:
            send_email_task.delay(sendmail)
            return {"message": f"Email sending task queued for {sendmail}"}
        except Exception as e:
            logging.error(f"Failed to queue email for {sendmail}: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to queue email task.")
    elif talktome:
        logging.info(f"Current time logged: {datetime.now()}")
        return {"message": "Current time logged."}
    return {"message": "No action specified."}


@app.get("/logs", response_class=PlainTextResponse)
async def get_logs():
    try:
        with open("messaging_system.log", "r") as f:
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read log file: {str(e)}")
