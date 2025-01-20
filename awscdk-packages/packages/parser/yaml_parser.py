import ast
import os
import string

import yaml
from yaml.loader import SafeLoader


def load_yaml(file: str, parse_env=False) -> dict:
    with open(file) as f:
        loader = __env_safe_loader() if parse_env else SafeLoader
        return yaml.load(f, Loader=loader)


def load_all_yaml(file: str, parse_env=False) -> list:
    with open(file) as f:
        loader = __env_safe_loader() if parse_env else SafeLoader
        return list(yaml.load_all(f, Loader=loader))


def __env_safe_loader():
    env_safe_loader = yaml.SafeLoader
    env_safe_loader.add_constructor('tag:yaml.org,2002:str',
                                    __str_constructor)
    token_re = string.Template.pattern
    env_safe_loader.add_implicit_resolver('tag:yaml.org,2002:str', token_re, None)
    return env_safe_loader


def __str_constructor(_, node):
    try:
        new_value = string.Template(node.value).substitute(dict(os.environ))
    except ValueError:
        return node.value

    if all(char in new_value for char in ['[', ']']):
        return ast.literal_eval(new_value)
    return new_value
