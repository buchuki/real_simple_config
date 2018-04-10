# Real Simple Config

Because I dislike all the other python config libraries, and it shouldn't have to
be hard.

All I wanted was a config system that:

* Was easy to set up
* Was easy to mock/test
* Was easy to get values out of
* Was easy for end users to write configuration for
* Was easy to supply defaults to

This config system allows the user to specify configs in the following ways:

* As an environment variable for each config lineitem
* As a yaml configuration file specified on the command line
* As a default yaml filename in their ~/.config directory
* As default values provided by the application developer

It tries each of these in order until it finds one.

Restrictions:
If you want to use environment variables to override settings, keep your yaml
files flat and have all values be strings.

## Installing

I haven't put it on pypi or even github, but it'll be something like

pip install git+https://github.com/buchuki/real_simple_config.git

## Using

To set up configuration, call init_config like so:

```python
    import real_simple
    real_simple.init_config(
        user_config,
        'my_app_default_config.yaml',
        'MYAPP_',
        {
            'FOO': 'def_value',
            'BAR': ''})
```

Where:

* `user_config` is an optional filename the user passed to you on the command
  line using your preferred command parsing library.
* `my_app_default_config.yaml` is the name of a file you want the user to read
  from in `~/.config` if they didn't explicitly pass a config file.
* `MYAPP_` is a prefix for environment variable lookup. Any key in the default
  dictionary can be looked up from a command-line with
  `export MYAPP_FOO='my_val'`.
* The dictionary is the list of default values for the configuration. Any key
  not in this dictionary will not be looked up in the user's config files or
  environment. So set defaults to None if you require the user to look them
  up.

To look up a configuration value, use:

```python
    from real_simple import conf
    val = conf('FOO')
```

## Testing

You can mock out `real_simple.init_config` or `real_simple.CONFIGURATION`
depending on your needs. The former would be mocked if your test code is called
before your app has called `init_config`. The latter would be mocked if you
want to specify mocked config values after `init_config` has been called. The
latter is the most likely case.
