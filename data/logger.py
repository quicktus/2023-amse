# very simple logger function for consistent logs
# based on https://github.com/Gallopsled/pwntools/blob/ab60471266de1858dea13b43f3e65c2b90d5530e/pwnlib/log.py

import datetime
from rich import print

msgtype_prefixes: dict = {
    "info":     ["bold",          "*"],  # noqa: E241
    "status":   ["bold magenta",  "x"],  # noqa: E241
    "success":  ["bold green",    "+"],  # noqa: E241
    "failure":  ["bold red",      "-"],  # noqa: E241
    "debug":    ["bold blue",     "DEBUG"],  # noqa: E241
    "error":    ["bold red",      "!"],  # noqa: E241
    "warning":  ["bold yellow",   "!"],  # noqa: E241
}


def log(message: str, msg_type: str = "info", timestamp=False, ret_str=False):
    prefix_style, prefix_text = msgtype_prefixes[msg_type]
    if prefix_style is None:
        # invalid or default style
        prefix_style, prefix_text = msgtype_prefixes["info"]

    time: str = (" " + datetime.datetime.now().strftime("%H:%M:%S")) if timestamp else ""
    # build message
    formatted_message = f"[[{prefix_style}]{prefix_text}[/{prefix_style}]]{time} {message}"

    if ret_str:
        return formatted_message
    else:
        print(formatted_message)
