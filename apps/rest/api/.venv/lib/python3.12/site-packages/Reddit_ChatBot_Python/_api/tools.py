import requests
from .._utils.consts import *
from .._utils.exceptions import APIException, BotNotRunning
import json
from .models import Channel, Message, Members, BannedUsers
from typing import Callable, Optional, Union, List
from .iconkeys import Reaction


def _get_user_id(username):
    response = requests.get(f"{WWW_REDDIT}/user/{username}/about.json", headers={'user-agent': WEB_USERAGENT}).json()
    u_id = response.get('data', {}).get('id')
    if u_id is None:
        return None
    else:
        return f't2_{u_id}'


class Tools:
    def __init__(self, reddit_auth, session_key_getter: Callable[[], str], is_running_getter: Callable[[], bool]):
        self.__reddit_auth = reddit_auth
        self.__req_sesh = requests.Session()
        self.__session_key_getter: Optional[Callable[[], str]] = session_key_getter
        self.__is_running_getter: Callable[[], bool] = is_running_getter

    def __handled_req(self, method: str, uri: str, chatmedia: bool, **kwargs) -> requests.Response:
        while self.__is_running_getter():
            if chatmedia:
                headers = {
                    'User-Agent': USER_AGENT,
                    'SendBird': SB_HEADER,
                    'SB-User-Agent': SB_USER_AGENT,
                    'Session-Key': self.__session_key_getter()
                }
            else:
                headers = {
                    'User-Agent': MOBILE_USERAGENT,
                    'Authorization': f'Bearer {self.__reddit_auth.api_token}',
                    'Content-Type': 'application/json',
                }
            response = self.__req_sesh.request(method, uri, headers=headers, **kwargs)
            if response.status_code == 401 and self.__reddit_auth.is_reauthable:
                new_access_token = self.__reddit_auth.refresh_api_token()
                headers.update({'Authorization': f'Bearer {new_access_token}'})
                continue
            elif response.status_code != 200:
                raise APIException(response.text)
            else:
                return response
        raise BotNotRunning("Cannot do that without running the bot first")

    def _get_invite_link(self, custom_type: str, expires_at: Optional[str] = None, max_joiners: int = 5,
                         channel_url: Optional[str] = None) -> dict:
        data = json.dumps({
            'id': 'd5d2819a6186',
            'variables': {
                'input': {'channelSendbirdId': channel_url, 'customType': custom_type, 'expiresAt': expires_at,
                          'maxJoiners': max_joiners}}
        })
        response = self.__handled_req(method='POST', uri=GQL_REDDIT, chatmedia=False, data=data)
        return response.json()

    def send_reaction(self, reaction_icon_key: Reaction, msg_id: Union[str, int], channel_url: str) -> None:
        data = json.dumps({
            "id": "7628b2213978",
            "variables": {
                "channelSendbirdId": channel_url,
                "messageSendbirdId": str(msg_id),
                "reactionIconKey": reaction_icon_key.value,
                "type": "ADD"
            }
        })
        self.__handled_req(method='POST', uri=GQL_REDDIT, chatmedia=False, data=data)

    def delete_reaction(self, reaction_icon_key: Reaction, msg_id: Union[str, int], channel_url: str) -> None:
        data = json.dumps({
            'id': '7628b2213978',
            'variables': {
                'channelSendbirdId': channel_url,
                'messageSendbirdId': msg_id,
                'reactionIconKey': reaction_icon_key.value,
                'type': 'DELETE'
            }
        })
        self.__handled_req(method='POST', uri=GQL_REDDIT, chatmedia=False, data=data)

    def rename_channel(self, name: str, channel_url: str) -> Channel:
        data = json.dumps({'name': name})
        response = self.__handled_req(method='PUT', uri=f"{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}",
                                      chatmedia=True,
                                      data=data)
        return Channel(response.json())

    def delete_message(self, channel_url: str, msg_id: int) -> None:
        self.__handled_req(method='DELETE',
                           uri=f"{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/messages/{msg_id}",
                           chatmedia=True)

    def kick_user(self, channel_url: str, user_id: str, duration: int) -> None:
        data = json.dumps({
            'channel_url': channel_url,
            'user_id': user_id,
            'duration': duration
        })
        self.__handled_req(method='POST', uri=f'{S_REDDIT}/api/v1/channel/kick/user',
                           chatmedia=False,
                           data=data)

    def invite_user_to_channel(self, channel_url: str, nicknames: Union[str, List[str]]) -> None:
        if isinstance(nicknames, str):
            nicknames = [nicknames]
        users = []
        for nickname in nicknames:
            users.append({'user_id': _get_user_id(nickname), 'nickname': nickname})
        data = json.dumps({'users': users})
        self.__handled_req(method='POST', uri=f'{S_REDDIT}/api/v1/sendbird/group_channels/{channel_url}/invite',
                           chatmedia=False,
                           data=data)

    def accept_chat_invite(self, channel_url):
        data = json.dumps({
            'user_id': self.__reddit_auth.user_id
        })
        response = self.__handled_req(method='PUT', uri=f'{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/accept',
                                      chatmedia=True, data=data)
        return Channel(response.json())

    def get_channels(self, limit: int = 100, order: str = "latest_last_message", show_member: bool = True,
                     show_read_receipt: bool = True, show_empty: bool = True, member_state_filter: str = "joined_only",
                     super_mode: str = "all", public_mode: str = "all", unread_filter: str = "all",
                     hidden_mode: str = "unhidden_only", show_frozen: bool = True,
                     # custom_types: str = 'direct,group'
                     ) -> List[Channel]:
        params = {
            'limit': limit,
            'order': order,
            'show_member': show_member,
            'show_read_receipt': show_read_receipt,
            'show_delivery_receipt': 'true',
            'show_empty': show_empty,
            'member_state_filter': member_state_filter,
            'super_mode': super_mode,
            'public_mode': public_mode,
            'unread_filter': unread_filter,
            'hidden_mode': hidden_mode,
            'show_frozen': show_frozen,
        }
        response = self.__handled_req(method='GET',
                                      uri=f'{SB_PROXY_CHATMEDIA}/v3/users/{self.__reddit_auth.user_id}/my_group_channels',
                                      chatmedia=True, params=params)
        return [Channel(channel) for channel in response.json()['channels']]

    def get_members(self, channel_url: str, next_token: str = None, limit: int = 20,
                    order: str = "member_nickname_alphabetical", member_state_filter: str = "all",
                    nickname_startswith: str = '') -> Members:
        params = {
            'token': next_token,
            'limit': limit,
            'order': order,
            'muted_member_filter': 'all',
            'member_state_filter': member_state_filter,
            'show_member_is_muted': 'true',
            'show_read_receipt': 'true',
            'show_delivery_receipt': 'true',
            'nickname_startswith': nickname_startswith
        }
        response = self.__handled_req(method='GET', uri=f'{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/members',
                                      chatmedia=True, params=params)
        return Members(response.json())

    def get_banned_members(self, channel_url, limit: int = 100) -> BannedUsers:
        params = {'limit': limit}
        response = self.__handled_req(method='GET', uri=f'{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/ban',
                                      chatmedia=True, params=params)
        return BannedUsers(response.json())

    def leave_chat(self, channel_url: str) -> None:
        data = json.dumps({
            'user_id': self.__reddit_auth.user_id
        })
        self.__handled_req(method='PUT', uri=f'{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/leave',
                           chatmedia=True, data=data)

    def create_channel(self, nicknames: List[str], group_name: str) -> Channel:
        users = []
        for nickname in nicknames:
            users.append({'user_id': _get_user_id(nickname), 'nickname': nickname})
        data = json.dumps({
            'users': users,
            'name': group_name
        })
        response = self.__handled_req(method='POST', uri=f'{S_REDDIT}/api/v1/sendbird/group_channels',
                                      chatmedia=False,
                                      data=data)
        return Channel(response.json())

    def hide_chat(self, channel_url: str, hide_previous_messages: bool = False, allow_auto_unhide: bool = True) -> None:
        data = json.dumps({
            'user_id': self.__reddit_auth.user_id,
            'hide_previous_messages': hide_previous_messages,
            'allow_auto_unhide': allow_auto_unhide
        })
        self.__handled_req(method='PUT', uri=f'{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/hide',
                           chatmedia=True, data=data)

    def unhide_chat(self, channel_url: str) -> None:
        self.__handled_req(method='DELETE', uri=f'{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/hide',
                           chatmedia=True)

    def get_older_messages(self, channel_url: str, message_ts: Union[int, str] = 9007199254740991,
                           custom_types: str = '*', prev_limit: int = 40, next_limit: int = 0,
                           reverse: bool = True) -> List[Message]:
        params = {
            'is_sdk': 'true',
            'prev_limit': prev_limit,
            'next_limit': next_limit,
            'include': 'false',
            'reverse': reverse,
            'message_ts': message_ts,
            'custom_types': custom_types,
            'with_sorted_meta_array': 'false',
            'include_reactions': 'false',
            'include_thread_info': 'false',
            'include_replies': 'false',
            'include_parent_message_text': 'false'
        }
        response = self.__handled_req(method='GET',
                                      uri=f'{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/messages',
                                      chatmedia=True, params=params)
        return [Message(msg) for msg in response.json()['messages']]

    def mute_user(self, channel_url: str, user_id: str, duration: int, description: str) -> None:
        data = json.dumps({
            'user_id': user_id,
            'seconds': duration,
            'description': description
        })
        self.__handled_req(method='POST', uri=f"{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/mute",
                           chatmedia=True, data=data)

    def unmute_user(self, channel_url: str, user_id: str) -> None:
        self.__handled_req(method='DELETE', uri=f"{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/mute/{user_id}",
                           chatmedia=True)

    def set_channel_frozen_status(self, channel_url: str, is_frozen: bool) -> None:
        data = json.dumps({
            'freeze': is_frozen,
        })
        self.__handled_req(method='PUT',
                           uri=f"{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}/freeze",
                           chatmedia=True, data=data)

    def delete_channel(self, channel_url: str) -> None:
        self.__handled_req(method='DELETE',
                           uri=f"{SB_PROXY_CHATMEDIA}/v3/group_channels/{channel_url}",
                           chatmedia=True)
