from ._ws_client import WebSockClient
import pickle
from .reddit_auth import _RedditAuthBase
from websocket import WebSocketConnectionClosedException
from ._api.tools import Tools
from ._api.models import Channel
from ._api.iconkeys import Snoo
from typing import Dict, List, Optional, Callable
from ._utils.frame_model import FrameType, FrameModel
from ._events import Events
from ._utils.exceptions import HookException

_hook = Callable[[FrameModel], Optional[bool]]


class ChatBot(Tools):
    def __init__(self, authentication: _RedditAuthBase, store_session: bool = True, log_error_frames: bool = True,
                 **kwargs):
        self.__r_authentication = authentication
        self._store_session = store_session
        if store_session:
            sb_access_token, user_id = self._load_session(authentication._get_repr_pkl())
        else:
            reddit_authentication = self.__r_authentication.authenticate()
            sb_access_token, user_id = reddit_authentication['sb_access_token'], reddit_authentication['user_id']

        self.__WebSocketClient = WebSockClient(access_token=sb_access_token, user_id=user_id, **kwargs)
        super().__init__(self.__r_authentication, self.__WebSocketClient.session_key_getter, self._is_running)
        self.__WebSocketClient.get_current_channels = self.get_channels

        self.event = Events(self.__WebSocketClient)

        if log_error_frames:
            self.event.on_any(func=lambda resp: self.__WebSocketClient.logger.error(resp), frame_type=FrameType.EROR,
                              run_parallel=True)
        self.__is_running = False

    def _is_running(self) -> bool:
        return self.__is_running

    def get_own_name(self) -> str:
        return self.__WebSocketClient.own_name

    def get_own_userid(self) -> str:
        return self.__WebSocketClient.user_id

    def get_chatroom_name_id_pairs(self) -> Dict[str, str]:
        return self.__WebSocketClient.channelid_sub_pairs

    def get_channelurl_by_name(self, channel_name: str) -> str:
        return next(key for key, val in self.__WebSocketClient.channelid_sub_pairs.items() if val == channel_name)

    def set_respond_hook(self, input_: str,
                         response: str,
                         limited_to_users: List[str] = None,
                         lower_the_input: bool = False,
                         exclude_itself: bool = True,
                         must_be_equal: bool = True,
                         limited_to_channels: List[str] = None
                         ) -> None:
        if limited_to_channels is None:
            limited_to_channels = []
        if limited_to_users is None:
            limited_to_users = []
        try:
            response.format(nickname="")
        except KeyError:
            raise HookException("You need to set a {nickname} key in welcome message!")

        def hook(resp: FrameModel) -> Optional[bool]:
            sent_message = resp.message.lower() if lower_the_input else resp.message
            if (resp.user.name in limited_to_users or not bool(limited_to_users)) \
                    and (exclude_itself and resp.user.name != self.__WebSocketClient.own_name) \
                    and ((must_be_equal and sent_message == input_) or (not must_be_equal and input_ in sent_message)) \
                    and (self.__WebSocketClient.channelid_sub_pairs.get(
                        resp.channel_url) in limited_to_channels or not bool(limited_to_channels)):
                response_prepped = response.format(nickname=resp.user.name)
                self.send_message(response_prepped, resp.channel_url)
                return True

        self.event.on_message(func=hook)

    def set_welcome_message(self, message: str, limited_to_channels: List[str] = None) -> None:
        if limited_to_channels is None:
            limited_to_channels = []
        try:
            message.format(nickname="", inviter="")
        except KeyError:
            raise HookException("Keys should be {nickname} and {inviter}")

        def hook(resp: FrameModel) -> Optional[bool]:
            if self.__WebSocketClient.channelid_sub_pairs.get(resp.channel_url) in limited_to_channels or \
                    not bool(limited_to_channels):
                response_prepped = message.format(nickname=resp.data.users[0].nickname,
                                                  inviter=resp.data.users[0].inviter.nickname)
                self.send_message(response_prepped, resp.channel_url)
                return True

        self.event.on_user_joined(hook)

    def set_farewell_message(self, message: str, limited_to_channels: List[str] = None) -> None:
        if limited_to_channels is None:
            limited_to_channels = []
        try:
            message.format(nickname="")
        except KeyError:
            raise HookException("Key should be {nickname}")

        def hook(resp: FrameModel) -> Optional[bool]:
            if self.__WebSocketClient.channelid_sub_pairs.get(resp.channel_url) in limited_to_channels or \
                    not bool(limited_to_channels):
                response_prepped = message.format(nickname=resp.data.nickname)
                self.send_message(response_prepped, resp.channel_url)
                return True

        self.event.on_user_left(hook)

    def remove_event_callback(self, func: _hook) -> None:
        self.__WebSocketClient.after_message_hooks.remove(func)

    def send_message(self, text: str, channel_url: str) -> None:
        self.__WebSocketClient.ws_send_message(text, channel_url)

    def send_snoomoji(self, snoomoji: Snoo, channel_url: str) -> None:
        self.__WebSocketClient.ws_send_snoomoji(snoomoji.value, channel_url)

    def send_gif(self, gif_url: str, channel_url: str, height: int = 200, width: int = 200) -> None:
        self.__WebSocketClient.ws_send_gif(gif_url, channel_url, height, width)

    def send_img(self, img_url: str, channel_url: str, height: int = 200, width: int = 200,
                 mimetype: str = "JPEG") -> None:
        self.__WebSocketClient.ws_send_img(img_url, channel_url, height, width, mimetype)

    def send_typing_indicator(self, channel_url: str) -> None:
        self.__WebSocketClient.ws_send_typing_indicator(channel_url)

    def stop_typing_indicator(self, channel_url: str) -> None:
        self.__WebSocketClient.ws_stop_typing_indicator(channel_url)

    def get_current_channels(self) -> List[Channel]:
        return self.__WebSocketClient.current_channels

    def run_4ever(self, auto_reconnect: bool = True, max_retries: int = 64, disable_ssl_verification: bool = False,
                  **kwargs) -> None:
        if disable_ssl_verification:
            import ssl
            sslopt = {"cert_reqs": ssl.CERT_NONE}
        else:
            sslopt = None

        self.__is_running = True
        for _ in range(max_retries):
            self.__WebSocketClient.ws.run_forever(ping_interval=15, ping_timeout=5,
                                                  skip_utf8_validation=True,
                                                  sslopt=sslopt,
                                                  **kwargs,
                                                  )
            if self.__WebSocketClient.is_logi_err and self.__r_authentication.is_reauthable:
                self.__WebSocketClient.logger.info("Re-Authenticating...")
                if self._store_session:
                    sb_access_token, _ = self._load_session(self.__r_authentication._get_repr_pkl(), force_reauth=True)
                else:
                    sb_access_token = self.__r_authentication.authenticate()['sb_access_token']
                self.__WebSocketClient.update_ws_app_urls_access_token(sb_access_token)
            elif not (
                    auto_reconnect and isinstance(self.__WebSocketClient.last_err, WebSocketConnectionClosedException)):
                break
            self.__WebSocketClient.logger.info("Auto Re-Connecting...")

    def close(self) -> None:
        self.__WebSocketClient.ws.close()

    def leave_chat(self, channel_url: str) -> None:
        super().leave_chat(channel_url)
        self.__WebSocketClient.update_channelid_sub_pair()

    def delete_channel(self, channel_url: str) -> None:
        super().delete_channel(channel_url)
        self.__WebSocketClient.update_channelid_sub_pair()

    def get_chat_invites(self) -> List[Channel]:
        return self.get_channels(member_state_filter="invited_only")

    # example expires at: 2023-01-01T23:00:00.000Z
    def get_own_invite_link(self, expires_at: Optional[str] = None, max_joiners: int = 5) -> str:
        return super()._get_invite_link(expires_at=expires_at, max_joiners=max_joiners, custom_type='DIRECT',
                                        channel_url=None)['data']['createChatChannelInviteLink']['inviteUrl']

    def get_invite_link(self, channel_url: str, expires_at: Optional[str] = None, max_joiners: int = 5):
        return super()._get_invite_link(expires_at=expires_at, max_joiners=max_joiners, custom_type='GROUP',
                                        channel_url=channel_url)['data']['createChatChannelInviteLink']['inviteUrl']

    def create_channel(self, nicknames: List[str], group_name: str) -> Channel:
        nicknames.append(self.__WebSocketClient.own_name)
        channel = super().create_channel(nicknames, group_name)
        self.__WebSocketClient.add_channelid_sub_pair(channel)
        return channel

    def create_direct_channel(self, nickname: str) -> Channel:
        channel = self.create_channel(nicknames=[self.__WebSocketClient.own_name, nickname], group_name="")
        self.__WebSocketClient.add_channelid_sub_pair(channel)
        return channel

    def accept_chat_invite(self, channel_url: str) -> Channel:
        group = super().accept_chat_invite(channel_url)
        self.__WebSocketClient.add_channelid_sub_pair(group)
        return group

    def rename_channel(self, name: str, channel_url: str) -> Channel:
        channel = super().rename_channel(name, channel_url)
        self.__WebSocketClient.update_channelid_sub_pair()
        return channel

    def _load_session(self, pkl_name, force_reauth=False):
        def get_store_file_handle(pkl_name_, mode_):
            try:
                return open(f"{pkl_name_}-stored.pkl", mode_)
            except FileNotFoundError:
                return None

        session_store_f = None if force_reauth else get_store_file_handle(pkl_name, 'rb')

        if session_store_f is None or force_reauth:
            session_store_f = get_store_file_handle(pkl_name, 'wb+')
            self.__r_authentication.authenticate()
            pickle.dump(self.__r_authentication, session_store_f)
        else:
            try:
                self.__r_authentication = pickle.load(session_store_f)
            except EOFError:
                return self._load_session(pkl_name, force_reauth=True)
        session_store_f.close()

        return self.__r_authentication.sb_access_token, self.__r_authentication.user_id
