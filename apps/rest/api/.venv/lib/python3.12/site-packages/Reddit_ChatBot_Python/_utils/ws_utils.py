import json
from urllib.parse import urlencode
from .consts import SB_USER_AGENT, SB_AI
from .._api.models import Channel, CustomType
from typing import List, Optional
import logging
import time


def mesg(channel_url: str, message, req_id: Optional[str], data: dict) -> dict:
    data = json.dumps({"v1": data}, separators=(',', ':'))
    mesg = json.dumps({"channel_url": channel_url, "message": message, "data": data, "mention_type": "users", "req_id": req_id}, separators=(',', ':'))
    return f'MESG{mesg}\n'


def mesg_text(channel_url: str, text: str, req_id: str) -> str:
    data = {"message_body": text, "embed_data": {}, "highlights": []}
    return mesg(channel_url=channel_url, message=text, req_id=req_id, data=data)


def mesg_snoo(channel_url: str, snoomoji: str, req_id: str) -> str:
    data = {"embed_data": {"site_name": "Reddit"}, "snoomoji": snoomoji}
    return mesg(channel_url=channel_url, message="", req_id=req_id, data=data)


def mesg_gif(channel_url: str, gif_url: str,  height: int, width: int) -> str:
    data = {"highlights": [], "gif": {"height": height, "url": gif_url, "width": width}}
    return mesg(channel_url=channel_url, message="", req_id=None, data=data)


def mesg_img(channel_url: str, img_url: str,  height: int, width: int, mimetype) -> str:
    data = {"highlights": [], "image": {"phase": "done", "height": height, "width": width, "url": img_url, "mimetype": mimetype}}
    return mesg(channel_url=channel_url, message="", req_id=None, data=data)


def tpst(channel_url: str) -> str:
    tpst = json.dumps({"channel_url": channel_url, "time": int(time.time() * 1000), "req_id": ""}, separators=(',', ':'))
    return f'TPST{tpst}\n'


def tpen(channel_url: str) -> str:
    tpen = json.dumps({"channel_url": channel_url, "time": int(time.time() * 1000), "req_id": ""}, separators=(',', ':'))
    return f'TPEN{tpen}\n'


def get_ws_url(user_id: str, access_token: str):
    socket_base = "wss://sendbirdproxyk8s.chat.redditmedia.com"
    ws_params = {
        "user_id": user_id,
        "access_token": access_token,
        "p": "Android",
        "pv": 30,
        "sv": "3.0.144",
        "ai": SB_AI,
        "SB-User-Agent": SB_USER_AGENT,
        "active": "1"
    }
    return f"{socket_base}/?{urlencode(ws_params)}"


def pair_channel_and_names(channels: List[Channel], own_user_id: str):
    channelid_sub_pairs = {}
    for channel in channels:
        chn_name = channel.name
        if channel.custom_type == CustomType.direct:
            for mmbr in channel.members:
                if mmbr.user_id != own_user_id:
                    chn_name = mmbr.nickname
                    break
        channelid_sub_pairs.update({channel.channel_url: chn_name})
    return channelid_sub_pairs


def configure_loggers():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter(fmt="%(asctime)s, %(levelname)s: %(message)s", datefmt="%H:%M"))
    ws_logger = logging.getLogger("websocket")
    ws_logger.propagate = False
    ws_logger.addHandler(sh)
    logger.addHandler(sh)
    return logger


def chat_printer(resp, channelid_sub_pairs):
    if resp.message == "":
        try:
            msg = resp.data.v1.snoomoji
        except AttributeError:
            msg = resp.message
    else:
        msg = resp.message
    print(f"{resp.user.name}@{channelid_sub_pairs.get(resp.channel_url)}: {msg}")
