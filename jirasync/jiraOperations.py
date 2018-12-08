#!/usr/bin/env python
# -- encoding: utf-8 --
#
# Copyright 2016 Telefónica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#
import json

import requests
import os
from requests.auth import HTTPBasicAuth
from jirasync.conf.settings import SEARCH_URI, CONTENT_TYPE
from functools import reduce
from jirasync.conf.settings import CEF_URL, CEF_USER, CEF_PASSWORD, CEF_PROJECTS, \
                                   FIWARE_URL, FIWARE_USER, FIWARE_PASSWORD, FIWARE_PROJECT, \
                                   ISSUE_URI, TRANSITION_URI
from jirasync.models import HelpDB, session
from http import HTTPStatus

__author__ = 'fla'


class Jira:
    def __init__(self, user, password, url, project):
        """
        Default constructor.
        :param user: The username of the jira account.
        :param password: The password of the jira account.
        :param url: The url of the Jira instance.
        :param project: The project in which we want to work.
        :return: The Jira instance.
        """
        self.user = user
        self.password = password
        self.url = url
        self.project = project

        if type(project) is list:
            projects = "(" + reduce(lambda x, y: x + ", " + y, self.project) + ")"
            operator = 'IN'
        else:
            projects = self.project
            operator = '='

        self.body = '''
        {
            "jql": "project %s %s",
            "fields": [
                "id",
                "reporter", 
                "key", 
                "issuetype", 
                "summary", 
                "priority", 
                "labels", 
                "status", 
                "environment", 
                "description", 
                "timeoriginalestimate",
                "project"
            ]
        }
        ''' % (operator, projects)

    def get_issues(self):
        """
        Resquest a list of issues from a Jira instance.
        :return: The list of issues in json format.
        """
        result = {}
        url = os.path.join(self.url, SEARCH_URI)
        headers = {'content-type': CONTENT_TYPE}

        response = requests.post(url=url, headers=headers, data=self.body,
                                 auth=HTTPBasicAuth(self.user, self.password), verify=False)

        info = json.loads(response.text, strict=False)

        info = list(filter(lambda x: x['fields']['status']['name'] == 'Open', info['issues']))

        return info

    def create_issues(self, issues):
        """
        Create issues in the FIWARE Jira.

        :return: The key value of the new jira issue.
        """

        keys = list(map(lambda x: self.create_issue(x), issues))

        return keys

    def create_issue(self, issue):
        """
        Create issues in the FIWARE Jira.

        :return: The key value of the new jira issue.
        """

        # curl -u user:password -X POST --data '{data}'
        #                          -H "Content-Type: application/json" https://jira.fiware.org/rest/api/2/issue

        description = "\\nIssueType:\\n{}\\n\\nEnvironment:\\n{}\\n\\nDescription:\\n{}".format(
                                                                            issue['fields']['issuetype']['name'],
                                                                            issue['fields']['environment'],
                                                                            issue['fields']['description']
                                                                            )

        payload = '''{
            "fields": {
                "project": {
                    "key": "%s"
                },
                "summary": "%s",
                "description": "%s",
                "issuetype": {
                    "name": "%s"
                },
                "assignee": {
                    "name":"%s"
                },
                "components": [
                    {
                        "name": "%s"
                    }
                ]
            }
        }''' % (self.project,
                issue['fields']['summary'],
                description,
                "testRequest",
                "fla",
                "Ops"
                )

        url = os.path.join(self.url, ISSUE_URI)
        headers = {'content-type': CONTENT_TYPE}

        response = requests.post(url=url, headers=headers, data=payload,
                                 auth=HTTPBasicAuth(self.user, self.password), verify=False)

        if response.status_code != 201:
            raise ValueError("Unexpected error, unable to create the issue")
        else:
            info = json.loads(response.text)

            result = {
                "fiware_key": info['key'],
                "cef_key": issue['key']
            }

            return result

    def get_transitions(self, issue_id, status):
        """
        Return the list of available transitions for a specific issue.

        :param issue_id: The id of the issue to check.
        :param status: The id of the issue to check.
        :return: the possible id status.
        """
        url = os.path.join(self.url, ISSUE_URI, issue_id, TRANSITION_URI)
        headers = {'content-type': CONTENT_TYPE}

        response = requests.get(url=url, headers=headers, auth=HTTPBasicAuth(self.user, self.password), verify=False)

        info = json.loads(response.text)

        # If we cannot find the status we return None value
        result = list(filter(lambda x: x['name'] == status, info['transitions']))
        result = result[0]['id']

        return result

    def update_status(self, issue_id, status):
        """
        Update the status of an issue through transition operations.

        :param issue_id: The id of the issue to update.
        :param status: The new status that we want to move.
        :return: Nothing.
        """
        url = os.path.join(self.url, ISSUE_URI, issue_id, TRANSITION_URI)
        headers = {'content-type': CONTENT_TYPE}

        transition_id = self.get_transitions(issue_id=issue_id, status=status)

        if transition_id is not None:
            payload = '''
            {
                "transition": {
                    "id":"%s"
                }
            }''' % transition_id

            response = requests.post(url=url, headers=headers, data=payload,
                                     auth=HTTPBasicAuth(self.user, self.password), verify=False)

            # Expected response 204
            if response.status_code != HTTPStatus.NO_CONTENT:
                raise ValueError("Unpexpected error")

        else:
            raise ValueError("The selected status cannot exist or cannot be accesible.")

    def update_issue(self, issue_id, comment):
        """
        Update a Jira issue with the values specified. Keep in mind that status is a transaction
        and have to be manage in a different way.

        :param issue_id: The issue to update.
        :param comment: The comment to add in the corresponding issue
        :return: Nothing.
        """
        payload = '''
        {
            "update": {
                "comment": [
                    {
                        "add": {
                            "body": "%s"
                        }
                    }
                ]
            }
        }''' % comment

        url = os.path.join(self.url, ISSUE_URI, issue_id)
        headers = {'content-type': CONTENT_TYPE}

        response = requests.put(url=url, headers=headers, data=payload,
                                auth=HTTPBasicAuth(self.user, self.password), verify=False)

        # Expected response 204
        if response.status_code != HTTPStatus.NO_CONTENT:
            raise ValueError("Unpexpected error")

    def update_components(self):
        print('TBImplemented')


if __name__ == '__main__':
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

    print(1)

