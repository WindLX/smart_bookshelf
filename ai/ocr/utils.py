from typing import Callable

def logger(func: Callable):
    """日志打印装饰器

    Args:
        func (callable): 待打印日志的函数
    """
    def wrapper(*args, **kwargs):
        print(f"Start [{func.__name__}]")
        result = func(*args, **kwargs)
        print(f"Finish [{func.__name__}]")
        return result
    return wrapper