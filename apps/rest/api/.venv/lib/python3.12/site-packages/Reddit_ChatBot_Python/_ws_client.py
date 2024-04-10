from typing import Callable
import websocket
import time
from ._utils.frame_model import get_frame_data, FrameType
from ._utils.ws_utils import get_ws_url, chat_printer, configure_loggers, pair_channel_and_names
from ._utils.ws_utils import mesg_gif, mesg_snoo, mesg_text, mesg_img, tpst, tpen
from ._utils.consts import *
from _thread import start_new_thread


class WebSockClient:
    def __init__(self, access_token, user_id, enable_trace=False, print_chat=True, log_websocket_frames=False,
                 other_logging=True):
        self.user_id = user_id

        self.channelid_sub_pairs = {}

        self.logger = configure_loggers()
        self.logger.disabled = not other_logging
        websocket.enableTrace(enable_trace)

        self.ws = self._get_ws_app(get_ws_url(self.user_id, access_token))

        self.req_id = int(time.time() * 1000)
        self.own_name = None
        self.print_chat = print_chat
        self.log_websocket_frames = log_websocket_frames
        self.last_err = None
        self.is_logi_err = False
        self.__session_key = None

        self.get_current_channels: Callable = None
        self.current_channels = None

        self.after_message_hooks = []
        self.parralel_hooks = []

    def session_key_getter(self):
        return self.__session_key

    def _get_ws_app(self, ws_url):
        ws = websocket.WebSocketApp(ws_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close,
                                    header={'User-Agent': USER_AGENT, 'Accept-Encoding': 'gzip'}
                                    )
        return ws

    def update_ws_app_urls_access_token(self, access_token):
        self.ws.url = get_ws_url(self.user_id, access_token)

    def on_message(self, _, message):
        resp = get_frame_data(message)
        if self.print_chat and resp.type_f == FrameType.MESG:
            chat_printer(resp, self.channelid_sub_pairs)
        if self.log_websocket_frames:
            self.logger.info(message)
        if resp.type_f == FrameType.LOGI:
            self.logger.info(message)
            self._logi(resp)

        for func in self.parralel_hooks:
            start_new_thread(func, (resp,))

        start_new_thread(self._response_loop, (resp,))

    def _response_loop(self, resp):
        for func in self.after_message_hooks:
            if func(resp):
                break

    def _logi(self, resp):
        try:
            logi_err = resp.error
        except AttributeError:
            logi_err = None
        if logi_err is None:
            self.is_logi_err = False
            self.last_err = None
            self.__session_key = resp.key
            self.update_channelid_sub_pair()
            self.own_name = resp.nickname
        else:
            self.logger.error(resp.message)
            self.is_logi_err = True

    def update_channelid_sub_pair(self):
        self.current_channels = self.get_current_channels(limit=100, order='latest_last_message', show_member=True,
                                                          show_read_receipt=True, show_empty=True,
                                                          member_state_filter='joined_only', super_mode='all',
                                                          public_mode='all', unread_filter='all',
                                                          hidden_mode='unhidden_only', show_frozen=True,
                                                          # custom_types='direct,group',
                                                          )
        self.channelid_sub_pairs = pair_channel_and_names(channels=self.current_channels,
                                                          own_user_id=self.user_id)

    def add_channelid_sub_pair(self, channel):
        self.current_channels.append(channel)
        self.channelid_sub_pairs = pair_channel_and_names(channels=self.current_channels,
                                                          own_user_id=self.user_id)

    def ws_send_message(self, text, channel_url):
        payload = mesg_text(channel_url=channel_url, text=text, req_id=self.req_id)
        self.ws.send(payload)
        self.req_id += 1

    def ws_send_snoomoji(self, snoomoji, channel_url):
        payload = mesg_snoo(channel_url=channel_url, snoomoji=snoomoji, req_id=self.req_id)
        self.ws.send(payload)
        self.req_id += 1

    def ws_send_gif(self, gif_url, channel_url, height, width):
        payload = mesg_gif(gif_url=gif_url, channel_url=channel_url, height=height, width=width)
        self.ws.send(payload)

    def ws_send_img(self, img_url, channel_url, height, width, mimetype):
        payload = mesg_img(img_url=img_url, channel_url=channel_url, height=height,
                           width=width, mimetype=mimetype)
        self.ws.send(payload)

    def ws_send_typing_indicator(self, channel_url):
        payload = tpst(channel_url=channel_url)
        self.ws.send(payload)

    def ws_stop_typing_indicator(self, channel_url):
        payload = tpen(channel_url=channel_url)
        self.ws.send(payload)

    def on_error(self, _, error):
        self.logger.error(error)
        self.last_err = error

    def on_close(self, *_):
        self.logger.warning("### websocket closed ###")
