# coding: utf-8

"""
настройки приложения
"""

import os

import yaml


class YamlSettingsMixin(object):

    def __init__(self):
        super(YamlSettingsMixin, self).__init__()

        self.config_path = os.path.join(self.BASE_DIR, 'settings.yaml')
        self.load()

    def load(self):
        with open(self.config_path) as stream:
            config = yaml.load(stream)
            if config:
                for key, value in config.iteritems():
                    if isinstance(value, dict):
                        for k, v in value.iteritems():
                            self_attr = getattr(self, key)
                            self_attr[k] = v
                    else:
                        setattr(self, key, value)

    def write(self):
        with open(self.config_path, 'w') as stream:
            save_settings = {
                key: getattr(self, key)
                for key in self.SAVED_SETTINGS if hasattr(self, key)
            }
            yaml.dump(save_settings, stream, default_flow_style=False, indent=4)


class SettingsModel(YamlSettingsMixin):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    BASE_CATALOG = BASE_DIR

    MAIN_WINDOW_MIN_HEIGHT = 600
    MAIN_WINDOW_MIN_WIDTH = 800

    MAIN_WINDOW_HEIGHT = 600
    MAIN_WINDOW_WIDTH = 800

    MAIN_WINDOW_X = 0
    MAIN_WINDOW_Y = 0

    DATE_TIME_FORMAT = u'%Y-%m-%d %H:%M:%S'
    DATE_TIME_FORMAT_EXIF = u'%Y:%m:%d %H:%M:%S'

    SAVED_SETTINGS = (
        'MAIN_WINDOW_MIN_HEIGHT',
        'MAIN_WINDOW_MIN_WIDTH',
        'MAIN_WINDOW_HEIGHT',
        'MAIN_WINDOW_WIDTH',
        'MAIN_WINDOW_X',
        'MAIN_WINDOW_Y',
        'BASE_CATALOG',
    )


settings = SettingsModel()
