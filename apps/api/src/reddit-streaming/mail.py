from protonmail import ProtonMail
import os
from dotenv import load_dotenv

load_dotenv()

PROTON_PASSPHRASE = os.getenv("PROTON_PASSPHRASE")

username = "jorge.lewis@futi.no"
password = PROTON_PASSPHRASE # Same as password lol

proton = ProtonMail()
proton.login(username, password)

private_key = 'privatekey.jorge.lewis@futi.no-6b01640941695dac59282e5eaee347ecac5dcac8.asc'
passphrase = PROTON_PASSPHRASE
proton.pgp_import(private_key, passphrase=passphrase)

# Send message
recipients = ["jorge.lewis@futi.no", "jonas.lindberg@futi.no", "joshua.heath@futi.no"]  # You can’t send to @proton.me/@protonmail.com yet
subject = "Testing push-notifications for relevant SM posts!"
body = "<html><body>Testing push-notifications for relevant social media posts!</body></html>"  # html or just text

new_message = proton.create_message(
    recipients=recipients,
    subject=subject,
    body=body
)

sent_message = proton.send_message(new_message)

# Save session, you do not have to re-enter your login, password, pgp key, passphrase
# WARNING: the file contains sensitive data, do not share it with anyone,
# otherwise someone will gain access to your mail.
proton.save_session('session.pickle')

# Load session
proton = ProtonMail()
proton.load_session('session.pickle', auto_save=True)
# Autosave is needed to save tokens if they are updated
# (the access token is only valid for 24 hours and will be updated automatically)

# Getting a list of all sessions in which you are authorized
proton.get_all_sessions()

# Revoke all sessions except the current one
proton.revoke_all_sessions()