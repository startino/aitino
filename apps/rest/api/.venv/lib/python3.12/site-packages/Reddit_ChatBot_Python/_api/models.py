from typing import Dict, Optional, List
from enum import Enum


class CustomType(str, Enum):
    group = 'group'
    direct = 'direct'


class MemberState(str, Enum):
    joined = 'joined'
    invited = 'invited'


class BannedUser:
    def __init__(self, in_data: dict):
        self.description: str = in_data.get('description')
        self.start_at: int = in_data.get('start_at')
        self.user: User = User(in_data.get('user'))
        self.end_at: int = in_data.get('end_at')


class BannedUsers:
    def __init__(self, in_data: dict):
        self.banned_list: List[BannedUser] = [BannedUser(n) for n in in_data.get('banned_list')]
        self.next: str = in_data.get('next')


class Channel:
    def __init__(self, in_data: dict):
        self.invited_at: Optional[int] = in_data.get('invited_at')
        self.custom_type: CustomType = CustomType[in_data.get('custom_type')]
        self.read_receipt: Dict[str] = in_data.get('read_receipt')
        self.member_state: MemberState = MemberState[in_data.get('member_state')]
        self.freeze: Optional[bool] = in_data.get('freeze')
        self.created_by: Optional[User] = User(in_data['created_by']) if in_data.get('created_by') is not None else None
        self.is_hidden: Optional[bool] = in_data.get('is_hidden')
        self.is_push_enabled: Optional[bool] = in_data.get('is_push_enabled')
        self.joined_ts: Optional[int] = in_data.get('joined_ts')
        self.is_created: Optional[bool] = in_data.get('is_created')
        self.member_count: Optional[int] = in_data.get('member_count')
        self.last_message: Optional[Message] = Message(in_data['last_message']) if in_data.get(
            'last_message') is not None else None
        self.user_last_read: Optional[int] = in_data.get('user_last_read')
        self.unread_mention_count: Optional[int] = in_data.get('unread_mention_count')
        self.channel_url: str = in_data.get('channel_url')
        self.operators: Optional[List] = in_data.get('operators')
        self.channel: _Channel = _Channel(in_data.get('channel'))
        self.unread_message_count: Optional[int] = in_data.get('unread_message_count')
        self.cover_url: Optional[str] = in_data.get('cover_url')
        self.members: List[User] = [User(n) for n in in_data.get('members')]
        self.is_public: Optional[bool] = in_data.get('is_public')
        self.joined_member_count: Optional[int] = in_data.get('joined_member_count')
        self.is_super: Optional[bool] = in_data.get('is_super')
        self.name: Optional[str] = in_data.get('name')
        self.created_at: Optional[int] = in_data.get('created_at')
        self.max_length_message: Optional[int] = in_data.get('max_length_message')
        self.inviter: Optional[User] = User(in_data.get('inviter'))
        self.count_preference: Optional[str] = in_data.get('count_preference')


class Members:
    def __init__(self, in_data: dict):
        self.members: List[User] = [User(n) for n in in_data.get('members')]
        self.next: str = in_data.get('next')


class Message:
    def __init__(self, in_data: dict):
        self.mentioned_users: List[User] = [User(n) for n in in_data.get('mentioned_users')]
        self.updated_at: Optional[int] = in_data.get('updated_at')
        self.is_op_msg: Optional[bool] = in_data.get('is_op_msg')
        self.is_removed: Optional[bool] = in_data.get('is_removed')
        self.user: Optional[User] = User(in_data['user']) if in_data.get('user') is not None else None
        self.message: str = in_data.get('message')
        self.data: str = in_data.get('data')
        self.type: Optional[str] = in_data.get('type')
        self.created_at: Optional[int] = in_data.get('created_at')
        self.req_id: Optional[str] = in_data.get('req_id')
        self.mention_type: Optional[str] = in_data.get('mention_type')
        self.channel_url: str = in_data.get('channel_url')
        self.message_id: Optional[int] = in_data.get('message_id')


class User:
    def __init__(self, in_data: dict):
        self.is_blocking_me: Optional[bool] = in_data.get('is_blocking_me')
        self.user_id: Optional[str] = in_data.get('user_id')
        self.is_muted: Optional[bool] = in_data.get('is_muted')
        self.friend_name: Optional[str] = in_data.get('friend_name')
        self.joined_ts: Optional[int] = in_data.get('joined_ts')
        self.is_active: Optional[bool] = in_data.get('is_active')
        self.read_ts: Optional[int] = in_data.get('read_ts')
        self.is_blocked_by_me: Optional[bool] = in_data.get('is_blocked_by_me')
        self.state: Optional[str] = in_data.get('state')
        self.role: Optional[str] = in_data.get('role')
        self.is_online: Optional[bool] = in_data.get('is_online')
        self.require_auth_for_profile_image: Optional[bool] = in_data.get('require_auth_for_profile_image')
        self.nickname: Optional[str] = in_data.get('nickname')


class _Channel:
    def __init__(self, in_data: dict):
        self.name: str = in_data.get('name')
        self.member_count: int = in_data.get('member_count')
        self.custom_type: CustomType = CustomType[in_data.get('custom_type')]
        self.channel_url: str = in_data.get('channel_url')
        self.created_at: int = in_data.get('created_at')
        self.max_length_message: int = in_data.get('max_length_message')
        self.data: str = in_data.get('data')
