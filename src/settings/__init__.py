# coding: utf-8

import os
import platform

import yaml

from settings.default_settings import *

if platform.system().lower() == 'windows':
    # необходимо поднять ещё на уровень выше, т.к. модули лежат в зип архиве
    # под винду использую py2exe
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
else:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

USER_HOME_DIR = os.path.expanduser('~')
LAST_CATALOG_DIR = USER_HOME_DIR

CATALOGS = []

config_path = os.path.join(BASE_DIR, 'settings.yaml')


def update(path):
    with open(path) as stream:
        config = yaml.load(stream)
    if config:
        gl = globals()
        for key, value in config.iteritems():
            if key in gl:
                if isinstance(value, dict):
                    for k, v in value.iteritems():
                        gl[key][k] = v
                else:
                    gl[key] = value

if os.path.exists(config_path):
    update(config_path)
