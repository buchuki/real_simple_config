import pytest

import real_simple


@pytest.fixture
def config_patch(monkeypatch):
    parsed_config = {}
    monkeypatch.setattr(real_simple, 'CONFIGURATION', parsed_config)
    return parsed_config


def test_no_config(config_patch):
    assert config_patch == {}
    assert config_patch is real_simple.CONFIGURATION
    real_simple.init_config(None, None, 'MY', {'a': 'b'})
    assert real_simple.CONFIGURATION == {'a': 'b'}
    assert real_simple.conf('a') == 'b'
    with pytest.raises(KeyError):
        real_simple.conf('b')


def test_yaml_config_overrides_exact_fields(config_patch, tmpdir):
    exact_yaml = '''
    ENVIRONMENT: 'dev'
    AWS_ACCESS_KEY_ID: 'hello'
    AWS_SECRET_ACCESS_KEY: 'hide me'
    '''
    yaml_path = tmpdir.join('config.yaml')
    with yaml_path.open('w') as file:
        file.write(exact_yaml)
    real_simple.init_config(
        str(yaml_path),
        None,
        'MY',
        {'ENVIRONMENT': 'TEST', 'AWS_ACCESS_KEY_ID': "", "AWS_SECRET_ACCESS_KEY": ""},
    )
    assert real_simple.CONFIGURATION == {
        'ENVIRONMENT': 'dev',
        'AWS_ACCESS_KEY_ID': 'hello',
        'AWS_SECRET_ACCESS_KEY': 'hide me',
    }


def test_yaml_config_defaults_and_extra_fields(config_patch, tmpdir):
    extra_yaml = '''
    NOT_A_FIELD: 'NOPE'
    '''
    yaml_path = tmpdir.join('config.yaml')
    with yaml_path.open('w') as file:
        file.write(extra_yaml)
    real_simple.init_config(
        str(yaml_path),
        None,
        'MY',
        {'ENVIRONMENT': 'TEST', 'AWS_ACCESS_KEY_ID': "", "AWS_SECRET_ACCESS_KEY": ""},
    )
    assert real_simple.CONFIGURATION == {
        'ENVIRONMENT': 'TEST', 'AWS_ACCESS_KEY_ID': '', 'AWS_SECRET_ACCESS_KEY': ''
    }


def test_yaml_config_file_not_exist(config_patch, tmpdir):
    yaml_path = tmpdir.join('not-config.yaml')
    real_simple.init_config(
        str(yaml_path),
        None,
        'MY',
        {'ENVIRONMENT': 'TEST', 'AWS_ACCESS_KEY_ID': "", "AWS_SECRET_ACCESS_KEY": ""},
    )
    assert real_simple.CONFIGURATION == {
        'ENVIRONMENT': 'TEST', 'AWS_ACCESS_KEY_ID': "", "AWS_SECRET_ACCESS_KEY": ""
    }


def test_enviro_config(config_patch, monkeypatch):
    monkeypatch.setenv('MY_ENVIRONMENT', 'dev')
    monkeypatch.setenv('MY_AWS_ACCESS_KEY_ID', 'hi')
    monkeypatch.setenv('MY_AWS_SECRET_ACCESS_KEY', 'there')

    real_simple.init_config(
        '',
        None,
        'MY',
        {'ENVIRONMENT': 'TEST', 'AWS_ACCESS_KEY_ID': "", "AWS_SECRET_ACCESS_KEY": ""},
    )
    assert real_simple.CONFIGURATION == {
        'ENVIRONMENT': 'dev',
        'AWS_ACCESS_KEY_ID': 'hi',
        'AWS_SECRET_ACCESS_KEY': 'there',
    }
