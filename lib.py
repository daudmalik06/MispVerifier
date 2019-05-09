#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from json import JSONEncoder
from ipaddress import ip_address, ip_network
import validators


class EncodeWarningList(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, WarningList):
            return obj.to_dict()
        return JSONEncoder.default(self, obj)


class PyMISPWarningListsError(Exception):
    def __init__(self, message):
        super(PyMISPWarningListsError, self).__init__(message)
        self.message = message


class WarningList():

    expected_types = ['string', 'substring', 'hostname', 'cidr']

    def __init__(self, warninglist, slow_search=False):
        self.warninglist = warninglist
        self.list = self.warninglist['list']
        self.description = self.warninglist['description']
        self.version = int(self.warninglist['version'])
        self.name = self.warninglist['name']
        if self.warninglist['type'] not in self.expected_types:
            raise Exception('Unexpected type, please update the expected_type list')
        self.type = self.warninglist['type']
        if self.warninglist.get('matching_attributes'):
            self.matching_attributes = self.warninglist['matching_attributes']

        self.slow_search = slow_search
        self._network_objects = []

        if self.slow_search and self.type == 'cidr':
            self._network_objects = self._network_index()
        # If network objects is empty, reverting to default anyway
        if not self._network_objects:
            self.slow_search = False

    def __contains__(self, value):
        if self.slow_search:
            return self._slow_search(value)
        return self._fast_search(value)

    def to_dict(self):
        to_return = {'list': [str(e) for e in self.list], 'name': self.name,
                     'description': self.description, 'version': self.version,
                     'type': self.type}
        if hasattr(self, 'matching_attributes'):
            to_return['matching_attributes'] = self.matching_attributes
        return to_return

    def to_json(self):
        return json.dumps(self, cls=EncodeWarningList)

    def _fast_search(self, value):
        return value in self.list

    def _network_index(self):
        to_return = []
        for entry in self.list:
            try:
                # Try if the entry is a network bloc or an IP
                to_return.append(ip_network(entry))
            except ValueError:
                pass
        return to_return

    def slowSearch(self, value, iocType):
        if self.type == 'string':
            # Exact match only, using fast search
            return self._fast_search(value)
        elif self.type == 'substring':
            # Expected to match on a part of the value
            # i.e.: value = 'blah.de' self.list == ['.fr', '.de']
            return any(v in value for v in self.list)
        elif self.type == 'hostname' and iocType == 'hostname':
            if validators.domain(value):
                for v in self.list:
                    if value in v:
                        return True
                return False
            else:
                # The value to search isn't a host, falling back to default
                return self._fast_search(value)

        elif self.type == 'cidr':
            try:
                value = ip_address(u"{ip}".format(ip=value))
            except ValueError:
                # The value to search isn't an IP address, falling back to default
                return self._fast_search(value)
            return any((value == obj or value in obj) for obj in self._network_objects)
