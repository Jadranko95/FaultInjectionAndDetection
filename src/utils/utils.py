import os


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        print(f"The environment variable {var_name} was not found.")
