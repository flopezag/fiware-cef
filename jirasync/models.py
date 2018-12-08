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
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jirasync.conf.settings import START_PROGRESS

__author__ = 'fla'

Base = declarative_base()


class Issue(Base):
    """
    Class to create the object of the DB.
    """
    __tablename__ = 'issues'

    cef_key = Column(String(20), primary_key=True)
    fiware_key = Column(String(20), nullable=False)


class HelpDB:
    """
    Class to help in the management of the Issues
    """

    @staticmethod
    def save_data(jira_fiware, jira_cef, data):
        # Check that the issue does not exist in the DB due to
        # it was not closed in the previous sprint.
        q = session.query(Issue).filter(Issue.cef_key == data['key']).first()

        if q is None:
            # Create new issues in the remote Jira.
            # Store the information into the DB.
            new_issue = Issue()

            new_issue.fiware_key = jira_fiware.create_issue(data)['fiware_key']
            new_issue.cef_key = data['key']

            session.add(new_issue)
            session.commit()

            # Log about the creation of the ticket for a specific user
            print("Created FIWARE issue {} for the CEF Issue {}".format(new_issue.fiware_key, new_issue.cef_key))

            # Make the transition of the CEF Ticket from Open to In Progress
            print("Making the transition of CEF Ticket")
            result = jira_cef.update_status(issue_id=new_issue.cef_key, status=START_PROGRESS)

            # Add a comment about starting to manage the issue.
            comment = "Hi {},\\n\\nThank you for the feedback!\\n\\nWe are working on your request, and we " \
                      "will get back to you soon with more details about the resolution of it.\\n\\nThanks again," \
                      "\\n\\nService Desk - Context Broker team".format(data['fields']['reporter']['displayName'])

            jira_cef.update_issue(issue_id=new_issue.cef_key, comment=comment)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///jirasync.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
