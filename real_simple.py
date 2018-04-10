from contextlib import suppress
import logging
import os

import yaml

log = logging.getLogger(__name__)

CONFIGURATION = {'a': 1}


def conf(name):
    return CONFIGURATION[name]


def init_config(yaml_filename, home_config_yaml, env_prefix, default_configuration):
    '''
    Config options come from:

    environment variables named <env_prefix>_<variable_name>
    or variable_name in yaml_filename (or ~/.config/home_config_yaml.yaml)
    or variable_name in default_configuration

    Ignores all variables in user-provided configs that don't also exist in
    `default_configuration`.

    To make it easy to modify configs with environment variables, there are no
    nested configs allowed and all values must be strings.

    Call `init_config` early, like so:

    ```
    real_simple.init_config(
        user_config,
        'my_app_default_config.yaml',
        'MYAPP_',
        {
            'FOO': 'def_value',
            'BAR': ''
        })

    To load a config value:

    ```
    import real_simple
    val = real_simple.conf('FOO')
    ```
    '''
    CONFIGURATION.update(default_configuration)

    if not yaml_filename:
        yaml_filename = os.path.expanduser(f'~/.config/{home_config_yaml}')

    if not yaml_filename or not os.path.exists(yaml_filename):
        logging.warn(f"'{yaml_filename}' does not exist")
        yaml_filename = None
    else:
        logging.info(f"Using config file {yaml_filename}")
    yaml_config = yaml.safe_load(open(yaml_filename)) if yaml_filename else {}

    print(os.environ)
    for key in default_configuration:
        with suppress(KeyError):
            CONFIGURATION[key] = yaml_config[key]
        with suppress(KeyError):
            CONFIGURATION[key] = os.environ[f'{env_prefix}_{key}']
