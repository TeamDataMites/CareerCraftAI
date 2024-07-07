import os
from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(
    prefix="/mail",
    tags=["mail"]
)


class EmailSchema(BaseModel):
    subject: str
    message: str


conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM = os.getenv("MAIL_FROM"),
    MAIL_PORT = 2525,
    MAIL_SERVER = "mail.smtp2go.com",
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=False,
    USE_CREDENTIALS = True
)


async def send_email_async(email: EmailSchema):
    message = MessageSchema(
        recipients=[os.getenv('MAIL_TO')],
        subject=email.subject,
        body=email.message,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

@router.post("/send-email/", summary="Send an email", description="Send an email to the complaint team.")
async def send_email(email: EmailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email_async, email)
    return {"message": "Email sent successfully."}
