#!/usr/bin/python

from charms.reactive import Endpoint
from charms.reactive import set_flag, clear_flag
from charms.reactive import when, when_not

class GenericDatabase(Endpoint):

    @when('endpoint.{endpoint_name}.joined')
    def _handle_joined(self):
        technology = self.all_joined_units.received['technology']
        dbname = self.all_joined_units.received['dbname']
        if technology:
            flag_t = 'endpoint.{endpoint_name}.' + technology + '.requested'
            set_flag(self.expand_name(flag_t))
        if dbname:
            flag_d = 'endpoint.{endpoint_name}.' + dbname + '.requested'
            set_flag(self.expand_name(flag_d))

    def technology(self):
        return self.all_joined_units.received['technology']

    def databasename(self):
        return self.all_joined_units.received['databasename']

    def username(self):
        return self.all_joined_units.received['username']

    def share_details(self, technology, host, dbname, user, password, port):
        for relation in self.relations:
            relation.to_publish['technology'] = technology
            relation.to_publish['host'] = host
            relation.to_publish['dbname'] = dbname
            relation.to_publish['user'] = user
            relation.to_publish['password'] = password
            relation.to_publish['port'] = port
