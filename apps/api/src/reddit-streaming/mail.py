import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime 
import diskcache as dc
from models import Submission

load_dotenv()

PROTON_PASSPHRASE = os.getenv("PROTON_PASSPHRASE") or ""
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or ""

def send_relevant_submission_via_email(submission: Submission):

    sender = 'jorge.lewis@futi.no'
    reciever = ['jorge.lewis@futi.no', 'jonas.lindberg@futi.no']
    msg = MIMEMultipart("alternative")
    msg['Subject'] = f'💸 Reddit Lead Found {submission.id}'
    text = f"""\
    A Reddit post has been found! 💸🎉 
    Title: {submission.title}
    URL: {submission.url}
    Datetime: {datetime.fromtimestamp(submission.created_utc)}
    """
    html = f"""\
    <html>
        <body>
            <h1>A Reddit post has been found! 💸🎉</h1> 
            Title: {submission.title} </br>
            URL: <a href="{submission.url}">{submission.url}</a> </br>
            Datetime: {datetime.fromtimestamp(submission.created_utc)} </br>
        </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    text_part = MIMEText(text, 'plain')
    html_part = MIMEText(html, 'html')

    # Add HTML/plain-text parts to MIMEMultipart message
    msg.attach(text_part)
    msg.attach(html_part)

    # Setup server and send email
    with smtplib.SMTP('127.0.0.1', 1025) as server:
        server.login(sender, SMTP_PASSWORD)
        server.sendmail(sender,reciever,msg.as_string())
