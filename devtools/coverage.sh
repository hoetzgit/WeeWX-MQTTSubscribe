#! /bin/bash
#
#    Copyright (c) 2020-2023 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
source ./devtools/python_versions.sh

export PYENV_VERSION=$weewx3_default_python_version
PYTHONPATH=bin coverage run -p --branch -m unittest discover bin/user/tests/unit; 

export PYENV_VERSION=$weewx4_default_python_version
PYTHONPATH=bin coverage3 run -p --branch -m unittest discover bin/user/tests/unit; 

coverage combine
coverage html --include bin/user/MQTTSubscribe.py
