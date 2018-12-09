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


class FilterData:
    @staticmethod
    def filter(data):
        result = list(map(lambda x: FilterData.__filter__(x), data))

        return result

    @staticmethod
    def __filter__(data):
        result = dict()

        result['key'] = data['key']
        result['comments'] = list(map(lambda x: FilterData.__get_data__(x), data['body']))

        return result

    @staticmethod
    def __get_data__(data):
        result = data['body']

        index = result.find('----')
        if index > -1:
            result = result[index+6:]

        result = result.replace('\n', '\\n').replace('\r', '\\r')

        return result

