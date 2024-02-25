import asyncio
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    List,
    Literal,
    Optional,
    Union,
)

from autogen import Agent, ConversableAgent, OpenAIWrapper
from fastapi import WebSocket

try:
    from termcolor import colored
except ImportError:

    def colored(x, *args, **kwargs):
        return x


class RetConversableAgent(ConversableAgent):
    def __init__(
        self,
        name: str,
        on_message: Any | None = None,
        websocket: WebSocket | None = None,
        system_message: Optional[Union[str, List]] = "You are a helpful AI Assistant.",
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Optional[str] = "TERMINATE",
        function_map: Optional[Dict[str, Callable]] = None,
        code_execution_config: Union[Dict, Literal[False]] = False,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        default_auto_reply: Union[str, Dict] = "",
        description: Optional[str] = None,
    ):
        """
        Args:
            name (str): name of the agent.
            system_message (str or list): system message for the ChatCompletion inference.
            is_termination_msg (function): a function that takes a message in the form of a dictionary
                and returns a boolean value indicating if this received message is a termination message.
                The dict can contain the following keys: "content", "role", "name", "function_call".
            max_consecutive_auto_reply (int): the maximum number of consecutive auto replies.
                default to None (no limit provided, class attribute MAX_CONSECUTIVE_AUTO_REPLY will be used as the limit in this case).
                When set to 0, no auto reply will be generated.
            human_input_mode (str): whether to ask for human inputs every time a message is received.
                Possible values are "ALWAYS", "TERMINATE", "NEVER".
                (1) When "ALWAYS", the agent prompts for human input every time a message is received.
                    Under this mode, the conversation stops when the human input is "exit",
                    or when is_termination_msg is True and there is no human input.
                (2) When "TERMINATE", the agent only prompts for human input only when a termination message is received or
                    the number of auto reply reaches the max_consecutive_auto_reply.
                (3) When "NEVER", the agent will never prompt for human input. Under this mode, the conversation stops
                    when the number of auto reply reaches the max_consecutive_auto_reply or when is_termination_msg is True.
            function_map (dict[str, callable]): Mapping function names (passed to openai) to callable functions, also used for tool calls.
            code_execution_config (dict or False): config for the code execution.
                To disable code execution, set to False. Otherwise, set to a dictionary with the following keys:
                - work_dir (Optional, str): The working directory for the code execution.
                    If None, a default working directory will be used.
                    The default working directory is the "extensions" directory under
                    "path_to_autogen".
                - use_docker (Optional, list, str or bool): The docker image to use for code execution.
                    Default is True, which means the code will be executed in a docker container. A default list of images will be used.
                    If a list or a str of image name(s) is provided, the code will be executed in a docker container
                    with the first image successfully pulled.
                    If False, the code will be executed in the current environment.
                    We strongly recommend using docker for code execution.
                - timeout (Optional, int): The maximum execution time in seconds.
                - last_n_messages (Experimental, int or str): The number of messages to look back for code execution.
                    If set to 'auto', it will scan backwards through all messages arriving since the agent last spoke, which is typically the last time execution was attempted. (Default: auto)
            llm_config (dict or False or None): llm inference configuration.
                Please refer to [OpenAIWrapper.create](/docs/reference/oai/client#create)
                for available options.
                To disable llm-based auto reply, set to False.
            default_auto_reply (str or dict): default auto reply when no code execution or llm-based reply is generated.
            description (str): a short description of the agent. This description is used by other agents
                (e.g. the GroupChatManager) to decide when to call upon this agent. (Default: system_message)
        """
        super().__init__(
            name,
            system_message,
            is_termination_msg,
            max_consecutive_auto_reply,
            human_input_mode,
            function_map,
            code_execution_config,
            llm_config,
            default_auto_reply,
            description,
        )
        self.on_message = on_message
        self.websocket = websocket

    def _print_received_message(
        self, message: dict | str, sender: Agent, carry_over: str = ""
    ) -> None:
        output = carry_over
        output += f"{sender.name} (to {self.name}):\n"

        message = self._message_to_dict(message)

        if message.get("tool_responses"):
            for tool_response in message["tool_responses"]:
                self._print_received_message(tool_response, sender, output)
            if message.get("role") == "tool":
                return  # If role is tool, then content is just a concatenation of all tool_responses

        if message.get("role") in ["function", "tool"]:
            if message["role"] == "function":
                id_key = "name"
            else:
                id_key = "tool_call_id"

            func_print = f"***** Response from calling {message['role']} \"{message[id_key]}\" *****"
            output += func_print + "\n"
            output += message["content"] + "\n"
            output += "*" * len(func_print) + "\n"
        else:
            content = message.get("content")
            if content is not None:
                if "context" in message:
                    content = OpenAIWrapper.instantiate(
                        content,
                        message["context"],
                        self.llm_config
                        and self.llm_config.get("allow_format_str_template", False),
                    )
                output += str(content) + "\n"
            if "function_call" in message and message["function_call"]:
                function_call = dict(message["function_call"])
                func_print = f"***** Suggested function Call: {function_call.get('name', '(No function name found)')} *****"
                output += func_print + "\n"
                output += (
                    "Arguments: \n"
                    + str(function_call.get("arguments", "(No arguments found)"))
                    + "\n"
                )
                output += "*" * len(func_print) + "\n"
            if "tool_calls" in message and message["tool_calls"]:
                for tool_call in message["tool_calls"]:
                    id = tool_call.get("id", "(No id found)")
                    function_call = dict(tool_call.get("function", {}))
                    func_print = f"***** Suggested tool Call ({id}): {function_call.get('name', '(No function name found)')} *****"
                    output += func_print + "\n"
                    output += (
                        "Arguments: \n"
                        + str(function_call.get("arguments", "(No arguments found)"))
                        + "\n"
                    )
                    output += "*" * len(func_print) + "\n"

        output += "\n" + "-" * 80 + "\n"
        if self.on_message:
            asyncio.run(self.on_message(output, self.websocket))
