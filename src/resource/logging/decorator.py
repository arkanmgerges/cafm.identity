"""
@author: Arkan M. Gerges<arkan.m.gerges@gmail.com>
"""


def debugLogger(f):
    import inspect
    import os

    blue = "\x1b[34;21m"
    green = "\x1b[32;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    magenta = "\u001b[45m"
    reset = "\x1b[0m"

    # link: https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    color1 = "\u001b[35m"
    color2 = "\u001b[33;1m"

    bgColor1 = "\u001b[43;1m"

    from src.resource.logging.logger import logger

    if os.getenv("DECORATOR_DEBUGGING_INFO_STATUS", True):

        def wrapper(*args, **kwargs):
            params = {}
            argsCount = len(args)
            count = 1
            while count < argsCount:
                params[f.__code__.co_varnames[count]] = args[count]
                count += 1
            params = {**params, **kwargs}
            fileName = inspect.getfile(f)
            className = args[0].__class__.__name__
            functionName = f.__code__.co_name

            logger.debug(
                f"{bgColor1}{color1} Debug Logger: {reset}\n{color1} Code execution entered {reset}{color2}[{className}.{functionName}]{reset}{color1} with parameters:{reset} {color2}{params}{reset}\n{color1}File: {reset}{color2}{fileName} {reset}"
            )

            return f(*args, **kwargs)

        return wrapper
    else:
        return f
