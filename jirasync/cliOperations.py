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
                                   ISSUE_URI, TRANSITION_URI, IN_PROGRESS, RESOLVE_ISSUE, CLOSE_ISSUE
from jirasync.models import Issue, HelpDB, session
from jirasync.filterData import FilterData

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
    print('Create new issues in FIWARE Jira based on CEF Jira issues...\n')

    jira_cef = Jira(user=CEF_USER,
                    password=CEF_PASSWORD,
                    url=CEF_URL,
                    project=CEF_PROJECTS)

    jira_fiware = Jira(user=FIWARE_USER,
                       password=FIWARE_PASSWORD,
                       url=FIWARE_URL,
                       project=FIWARE_PROJECT)

    issues = jira_cef.get_issues()

    list(map(lambda x: HelpDB.save_data(jira_cef=jira_cef, jira_fiware=jira_fiware, data=x), issues))

    session.close()

    print('\n\n')


@jirasync.command()
def status(**kwargs):
    """
    Get the current list of issues that are not closed in CEF.

    :return: Nothing.
    """
    print('List all the issues in the DB whose status is not closed in sprint:\n')

    issues = session.query(Issue).all()

    list(map(lambda x: print('    * CEF key: {}        FIWARE key: {}'.format(x.cef_key, x.fiware_key)), issues))

    session.close()

    print('\n\n')


@jirasync.command()
def update(**kwargs):
    """
    Update the CEF issues with the comment of closed FIWARE issues.

    :return: Nothing.
    """
    print('Update all the issues whose attributes do not match the previous stored one in sprint...\n')

    issues_db = session.query(Issue).all()

    jira_cef = Jira(user=CEF_USER,
                    password=CEF_PASSWORD,
                    url=CEF_URL,
                    project=CEF_PROJECTS)

    jira_fiware = Jira(user=FIWARE_USER,
                       password=FIWARE_PASSWORD,
                       url=FIWARE_URL,
                       project=FIWARE_PROJECT)

    # 1st: Get the list of issues from DB and filter them to get only the closed one.
    dict_keys = dict((k.fiware_key, k.cef_key) for k in issues_db)
    keys = list(dict_keys.keys())
    keys = jira_fiware.filter_search(keys)

    # 2nd: Get the list of comments
    comments_issues = list(map(lambda x: jira_fiware.search_comments_issues(x), keys))

    # 3rd: Filter the content of the comments to eliminate email content
    comments_issues = FilterData.filter(data=comments_issues)

    # 4th: Create the comments in the CEF Jira issues
    jira_cef.add_comments_issues(comments=comments_issues, dict_keys=dict_keys)

    # 5th: Delete the closed JIRA issues from the DB
    cef_keys = list(map(lambda x: dict_keys[x], keys))
    list(map(lambda x: HelpDB.delete_data(x), cef_keys))

    # 6th: Close the CEF Jira issue, it is two transitions, from 'In Progress' to
    #      'Resolve Issue' and from 'Resolve Issue' to 'Close'
    list(map(lambda x: jira_cef.update_status(issue_id=x, status=RESOLVE_ISSUE), cef_keys))
    list(map(lambda x: jira_cef.update_status(issue_id=x, status=CLOSE_ISSUE), cef_keys))

    print('\n\n')


@jirasync.command()
def sync(**kwargs):
    """
    Make the complete synchronization of CEF and FIWARE Jiras.

    :return: Nothing
    """
    print("Synchronizing the jira's tickets...\n\n")
    create(kwargs)
    update(kwargs)

    print('\n\n')
