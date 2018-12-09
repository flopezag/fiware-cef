#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2018 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##
from configparser import ConfigParser
import logging
import os.path

config = ConfigParser()

"""
Default configuration.

The configuration `cfg_defaults` are loaded from `cfg_filename`, if file exists in
/etc/fiware.d/jirasync.ini

Optionally, user can specify the file location manually using an Environment variable
called CEF_SYNC_CONFIGFILE.
"""

name = 'jirasync'

cfg_dir = "/etc/fiware.d"

if os.environ.get("CEF_SYNC_CONFIGFILE"):
    cfg_filename = os.environ.get("CEF_SYNC_CONFIGFILE")
    cfg_dir = os.path.dirname(cfg_filename)

else:
    cfg_filename = os.path.join(cfg_dir, '%s.ini' % name)

Config = ConfigParser()

Config.read(cfg_filename)


def check_log_level(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)

    if not isinstance(numeric_level, int):
        print('Invalid log level: {}'.format(loglevel))
        exit()

    return numeric_level


def config_section_map(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except Exception:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


if Config.sections():
    # Data CEF JIRA section
    cef_section = config_section_map("cef_jira")
    CEF_URL = cef_section['url']
    CEF_PROJECTS = cef_section['projects'].split(",")
    CEF_USER = cef_section['user']
    CEF_PASSWORD = cef_section['password']

    # Data FIWARE JIRA section
    fiware_section = config_section_map("fiware_jira")
    FIWARE_URL = fiware_section['url']
    FIWARE_PROJECT = fiware_section['project']
    FIWARE_USER = fiware_section['user']
    FIWARE_PASSWORD = fiware_section['password']

    # Data for JIRA section
    jira_section = config_section_map("jira")
    SEARCH_URI = jira_section['search_uri']
    CONTENT_TYPE = jira_section['content_type']
    ISSUE_URI = jira_section['issue_uri']
    TRANSITION_URI = jira_section['transition_uri']

    # DATA FOR Transition section
    transition_section = config_section_map("transition")
    START_PROGRESS = transition_section['start_progress']
    CLOSE_ISSUE = transition_section['close_issue']
    IN_PROGRESS = transition_section['in_progress']
    RESOLVE_ISSUE = transition_section['resolve_issue']

    # Data from Log section
    log_section = config_section_map("log")
    LOG_LEVEL = check_log_level(log_section['loglevel'])
else:
    msg = '\nERROR: There is not defined CEF_SYNC_CONFIGFILE environment variable ' \
          '\n       pointing to configuration file or there is no jirasync.ini file' \
          '\n       in the /etd/init.d directory.' \
          '\n\n       Please correct at least one of them to execute the program.'
    exit(msg)

# Settings file is inside Basics directory, therefore I have to go back to the parent directory
# to have the Code Home directory
CODE_HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_HOME = os.path.join(CODE_HOME, 'log')
LOG_FILE = 'Jirasync.log'

# DEFINITION OF TRANSACTION BETWEEN JIRA'S
remote_issuetype = {'Task': 'WorkItem', 'Bug': 'Bug', 'User Story': 'Story'}

remote_project = {'Aiakos': 'OPS', 'Bosun - Policy Manager': 'CLD', 'FIHealth': 'OPS', 'GlanceSync': 'OPS',
                  'Monitoring GE': 'OPS', 'Murano': 'CLD', 'Pegasus - PaaS Manager': 'CLD',
                  'Puppet-Wrapper': 'CLD', 'Sagitta - SDC Manager': 'CLD', 'UserManagement': 'OPS',
                  'lab:spain': 'LAB', 'FIWARE Lab:Spain': 'LAB', 'Lab:Spain': 'LAB'
                  }

remote_component = {'Aiakos': 'FI-Toolkit', 'Bosun - Policy Manager': 'Policy Manager - Bosun', 'FIHealth': 'FI-Health',
                    'GlanceSync': 'FI-Toolkit', 'Monitoring GE': 'FI-Health', 'Murano': 'Murano',
                    'Pegasus - PaaS Manager': 'PaaS - Pegasus', 'Puppet-Wrapper': 'SDC - Sagitta',
                    'Sagitta - SDC Manager': 'SDC - Sagitta', 'UserManagement': 'FI-Toolkit',
                    'FIWARE Lab:Spain': 'NODE_SPAIN', 'Lab:Spain': 'NODE_SPAIN'}

remote_users = {'gjp465': 'gjimenez', 'henar': 'henar', 'fla': 'fla', 'jicg': 'jicg',
                'jesuspg': 'jesus.perezgonzalez', 'None': 'None', 'pra': 'pra', 'jfr39': 'fla'}
