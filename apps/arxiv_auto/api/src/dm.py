from reddit_utils import REDDIT_PASSWORD, get_subreddits, reply
from Reddit_ChatBot_Python import ChatBot, RedditAuthentication
from Reddit_ChatBot_Python import CustomType, Snoo, Reaction
from dotenv import load_dotenv
import os

load_dotenv()

REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")


first_dm = """

"""

second_dm = """

"""

third_dm = """

"""

# create authentication with username and pass
reddit_authentication = RedditAuthentication.PasswordAuth(
    reddit_username="antopia_hk",
    reddit_password=REDDIT_PASSWORD,
)  # 2FA supported, default'd to None


# instantiate the chatbot
chatbot = ChatBot(
    print_chat=True,
    store_session=True,
    log_websocket_frames=False,  # some parameters u might wanna know
    authentication=reddit_authentication,
)


# starting a direct chat
@chatbot.event.on_ready
def dm_chat(_):
    dm_channel = chatbot.create_direct_channel("eksno")
    chatbot.send_message("Hey what's up?", dm_channel.channel_url)


chatbot.run_4ever(auto_reconnect=True)

