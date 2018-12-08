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
"""Synchronise two Jira instances.

Usage:
  jirasync create     Create the Sprint and store the issues into the DB.
  jirasync upgrade    Check all the Local issues and check which is updated
                      and upgrade the changes to the Remote Jira.
  jirasync list       List all the Local issues (from DB) whose status is not closed.
  jirasync sync       Complete all the cycle of create, upgrade and list of Jira issues.

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

from jirasync.cliOperations import jirasync
import certifi
import urllib3

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

__version__ = '1.0.0'

__author__ = 'fla'


if __name__ == '__main__':
    """
    jirasync create          Create the Sprint and store the issues into the DB.
    jirasync upgrade         Check all the Local issues and check which is updated
                             and upgrade the changes to the Remote Jira.
    jirasync list            List all the Local issues (from DB) whose status is not closed.
    jirasync sync            Complete all the cycle of create, upgrade and list of Jira issues.
    """
    version = "Synchronise two Jira instances v{}".format(__version__)

    jirasync()
