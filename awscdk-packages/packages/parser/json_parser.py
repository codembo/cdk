import os


def from_json(file: str, parse_env=False):
    with open(file, "r") as f:
        file_data = f.read()
        if parse_env:
            for key in os.environ:
                file_data = file_data.replace('${' + key + '}', os.environ[key])
            return file_data
        return file_data
