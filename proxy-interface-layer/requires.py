#!/usr/bin/python

from charms.reactive import Endpoint
from charms.reactive import when, when_not
from charms.reactive import set_flag, clear_flag
from charms.reactive import data_changed

class GenericDatabaseClient(Endpoint):

    @when('endpoint.{endpoint_name}.changed')
    def _handle_technology_available(self):
        if self.technology():
            set_flag(self.expand_name('endpoint.{endpoint_name}.available'))

    def request(self, technology, databasename, username):
        for relation in self.relations:
            relation.to_publish['technology'] = technology
            relation.to_publish['databasename'] = databasename
            relation.to_publish['username'] = username

    def technology(self):
        """
        Return the technology of the generic database.
        """
        return self.all_joined_units.received['technology']

    def databasename(self):
        """
        Return the name of the provided database.
        """
        return self.all_joined_units.received['dbname']

    def host(self):
        """
        Return the host for the provided database.
        """
        return self.all_joined_units.received['host']

    def port(self):
        """
        Return the port the provided database.
        """
        return self.all_joined_units.received['port']

    def user(self):
        """
        Return the username for the provided database.
        """
        return self.all_joined_units.received['user']

    def password(self):
        """
        Return the password for the provided database.
        """
        return self.all_joined_units.received['password']
