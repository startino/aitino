import smtplib
from arxiv import Result
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime
import markdown

load_dotenv()

PROTON_PASSPHRASE = os.getenv("PROTON_PASSPHRASE") or ""
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or ""


def email_articles(results: list[Result]):
    sender = "jorge.lewis@futi.no"
    receiver = [
        "jorge.lewis@futi.no",
    ]
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Daily Arxiv Summary - {datetime.now().strftime('%Y-%m-%d')}"
    msg["From"] = sender
    msg["To"] = ", ".join(receiver)

    text = "Daily Arxiv Summary:\n\n" + "\n---\n".join(
        f"Title: {result.title}\nSummary: {result.summary}\nLink: {result.pdf_url}"
        for result in results
    )

    html = f"""\
    <html>
      <body>
        <h1>Daily Arxiv Summary</h1>
        <ul>
          {''.join(
            f'<li><h2>{result.title}</h2><p>{result.summary}</p><p><a href="{result.entry_id}">Read more</a></p></li>'
            for result in results
          )}
        </ul>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    text_part = MIMEText(text, "plain")
    html_part = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    msg.attach(text_part)
    msg.attach(html_part)

    # Setup server and send email
    with smtplib.SMTP("smtp.protonmail.ch", 587) as server:
        server.starttls()
        server.login(sender, SMTP_PASSWORD)
        server.sendmail(sender, receiver, msg.as_string())
