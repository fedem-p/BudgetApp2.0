"""General utils functions."""
import ast


def dict2str(my_dict: dict) -> str:
    "Return dictionary as string."
    return str(my_dict)


def str2dict(my_str: str) -> dict:
    "Return string as dictionary."
    return ast.literal_eval(my_str)
