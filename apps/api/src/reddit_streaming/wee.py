
from datetime import datetime, timedelta
from interfaces import db

from models.lead import Lead

lead = Lead(
    redditor="antopia_hk",
    last_contacted_at=datetime.now()-timedelta(days=4),
    source="Reddit",
    last_event="comment_posted",
    status="subscriber",
    title="Hello",
    body="Hello, I am interested in your product.")
db.post_lead(lead)

leads = db.get_due_leads()

if leads is not None:
    print(''.join([f"Lead: {lead.last_contacted_at} \n" for lead in leads]))
