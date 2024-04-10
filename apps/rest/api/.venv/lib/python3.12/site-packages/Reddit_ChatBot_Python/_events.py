from typing import Callable, Optional
from ._utils.frame_model import FrameType, FrameModel

_hook = Callable[[FrameModel], Optional[bool]]


class Events:
    def __init__(self, ws_client):
        self.ws_client = ws_client
        self.__ready_executed = False

    def on_any(self, func: Optional[_hook] = None, frame_type: FrameType = FrameType.MESG, run_parallel=False):
        def wrap(func):
            def hook(resp: FrameModel):
                if resp.type_f == frame_type:
                    return func(resp)

            if run_parallel:
                self.ws_client.parralel_hooks.append(hook)
            else:
                self.ws_client.after_message_hooks.append(hook)

        if func is None:
            return wrap

        return wrap(func)

    def on_reaction(self, func: Optional[_hook] = None, run_parralel=False):
        def wrap(func):
            return self.on_any(func, FrameType.MRCT, run_parralel)

        if func is None:
            return wrap

        return wrap(func)

    def on_image(self, func: Optional[_hook] = None, run_parralel=False):
        def wrap(func):
            return self.on_any(func, FrameType.MEDI, run_parralel)

        if func is None:
            return wrap

        return wrap(func)

    def on_broadcast(self, func: Optional[_hook] = None, run_parralel=False):
        def wrap(func):
            return self.on_any(func, FrameType.BRDM, run_parralel)

        if func is None:
            return wrap

        return wrap(func)

    def on_message(self, func: Optional[_hook] = None, run_parallel=False):
        def wrap(func):
            return self.on_any(func, FrameType.MESG, run_parallel)

        if func is None:
            return wrap

        return wrap(func)

    def on_ready(self, func: Optional[_hook] = None):
        def wrap(func):
            def hook(resp: FrameModel) -> Optional[bool]:
                try:
                    _ = resp.error
                    return
                except AttributeError:
                    pass
                if self.__ready_executed:
                    return
                else:
                    self.__ready_executed = True
                return func(resp)

            return self.on_any(hook, FrameType.LOGI, False)

        if func is None:
            return wrap

        return wrap(func)

    def on_user_read(self, func: Optional[_hook] = None, run_parallel=False):
        def wrap(func):
            return self.on_any(func, FrameType.READ, run_parallel)

        if func is None:
            return wrap

        return wrap(func)

    def on_invitation(self, func: Optional[_hook] = None, run_parallel=False):
        def wrap(func):
            def hook(resp: FrameModel) -> Optional[bool]:
                try:
                    _ = resp.data.inviter
                    if not any([invitee.nickname == self.ws_client.own_name for invitee in resp.data.invitees]):
                        return
                except AttributeError:
                    return
                return func(resp)

            return self.on_any(hook, FrameType.SYEV, run_parallel)

        if func is None:
            return wrap

        return wrap(func)

    def on_invitation_of_other(self, func: Optional[_hook] = None, run_parallel=False):
        def wrap(func):
            def hook(resp: FrameModel) -> Optional[bool]:
                try:
                    _ = resp.data.inviter
                    if resp.cat != 10020:
                        return
                except AttributeError:
                    return

                return func(resp)

            return self.on_any(hook, FrameType.SYEV, run_parallel)

        if func is None:
            return wrap

        return wrap(func)

    def on_message_deleted(self, func: Optional[_hook] = None, run_parallel=False):
        def wrap(func):
            return self.on_any(func, FrameType.DELM, run_parallel)

        if func is None:
            return wrap

        return wrap(func)

    def on_user_joined(self, func: Optional[_hook] = None, run_parallel=False):
        def wrap(func):
            def hook(resp: FrameModel) -> Optional[bool]:
                try:
                    _ = resp.data.users[0].nickname
                    _ = resp.data.users[0].inviter.nickname
                except (AttributeError, IndexError):
                    return
                return func(resp)

            return self.on_any(hook, FrameType.SYEV, run_parallel)

        if func is None:
            return wrap

        return wrap(func)

    def on_user_left(self, func: Optional[_hook] = None, run_parallel=False):
        def wrap(func):
            def hook(resp: FrameModel) -> Optional[bool]:
                try:
                    _ = resp.channel.disappearing_message
                    _ = resp.data.nickname
                except AttributeError:
                    return
                return func(resp)

            return self.on_any(hook, FrameType.SYEV, run_parallel)

        if func is None:
            return wrap

        return wrap(func)

    def on_user_typing(self, func: Optional[_hook] = None, run_parallel=False):
        def wrap(func):
            def hook(resp: FrameModel) -> Optional[bool]:
                try:
                    _ = resp.data.nickname
                    if resp.cat != 10900:
                        return
                except AttributeError:
                    return

                return func(resp)

            return self.on_any(hook, FrameType.SYEV, run_parallel)

        if func is None:
            return wrap

        return wrap(func)
