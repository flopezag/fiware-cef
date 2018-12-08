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
from jirasync.jiraOperations import Jira
from jirasync.conf.settings import CEF_URL, CEF_USER, CEF_PASSWORD, CEF_PROJECTS, \
                                   FIWARE_URL, FIWARE_USER, FIWARE_PASSWORD, FIWARE_PROJECT, \
                                   ISSUE_URI, TRANSITION_URI
from jirasync.models import HelpDB, session

__author__ = 'fla'

import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def jirasync():
    pass


@jirasync.command()
def create(**kwargs):
    """
    Generate the FIWARE issues with the CEF issues open.

    :return: Nothing.
    """
    jira_cef = Jira(user=CEF_USER,
                    password=CEF_PASSWORD,
                    url=CEF_URL,
                    project=CEF_PROJECTS)

    jira_fiware = Jira(user=FIWARE_USER,
                       password=FIWARE_PASSWORD,
                       url=FIWARE_URL,
                       project=FIWARE_PROJECT)

    issues = jira_cef.get_issues()

    issues = list(map(lambda x: HelpDB.save_data(jira_cef=jira_cef, jira_fiware=jira_fiware, data=x), issues))

    session.close()


@jirasync.command()
def status(**kwargs):
    """
    Get the current list of issues that are not closed in CEF.

    :param sprint: Sprint in the local Jira.
    :return: Nothing.
    """
    print('List all the issues in the DB whose status is not closed in sprint:\n')

    '''
    i = 1
    for issue in session.query(Issue).all():
        if issue.status != 'Closed':
            print('    ({}): Local key: {}        Remote key: {}        Status: {}'
                  .format(str(i), issue.key, issue.remotekey, issue.status))
            i += 1
    '''


@jirasync.command()
def update(**kwargs):
    """
    Update the CEF issues with the comment of closed FIWARE issues.

    :return: Nothing.
    """
    print('Update all the issues whose attributes do not match the previous stored one in sprint.\n')


@jirasync.command()
def sync(**kwargs):
    """
    Make the complete synchronization of CEF and FIWARE Jiras.

    :return: Nothing
    """
    print("To be implemented")
