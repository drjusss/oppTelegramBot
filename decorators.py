import typing
import functools
import datetime
import traceback


def log_error(func: typing.Callable) -> typing.Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> typing.Any:
        try:
            func(*args, **kwargs)
        except Exception as ex:
            traceback_string = traceback.format_exc()
            with open(file='exceptions.txt', mode='a', encoding='utf-8') as file:
                file.write(f'[{func.__name__}]({datetime.datetime.now()})\n{traceback_string}\n\n' + '=' * 50 + '\n\n')
    return wrapper
