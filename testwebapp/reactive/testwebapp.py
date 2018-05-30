#!/usr/bin/python

import pwd
import os
from subprocess import call
from charmhelpers.core import host
from charmhelpers.core.hookenv import log, status_set, config
from charmhelpers.core.templating import render
from charms.reactive import when, when_not, set_flag, clear_flag, when_file_changed, endpoint_from_flag
from charms.reactive import Endpoint

###########################################################################
#                                                                         #
# Installation of apache + waiting for generic-database (provider) charm  #
#                                                                         #
###########################################################################

@when('apache.available')
def finishing_up_setting_up_sites():
    host.service_reload('apache2')
    set_flag('apache.start')


@when('apache.start')
@when_not('endpoint.database.connected')
def waiting_for_db():
    host.service_reload('apache2')
    status_set('maintenance', 'Waiting for a generic database relation')


########################################################################
#                                                                      #
# Request of database technology to generic-database (provider charm)  #
#                                                                      #
########################################################################

@when('endpoint.database.joined')
@when_not('endpoint.database.connected')
def request_mysql_db():
    endpoint = endpoint_from_flag('endpoint.database.joined')
    endpoint.request('mysql', 'mydbname', 'myuser')
    status_set('maintenance', 'Requesting mysql gdb')


##################################################
#                                                #
# Request successful, get data and render config # 
#                                                #
##################################################


@when('endpoint.database.available')
def mysql_render_config():
    
    mysql = endpoint_from_flag('endpoint.database.available')

    render('database-config.j2', '/var/www/testwebapp/database-config.html', {
        'gdb_host' : mysql.host(),
        'gdb_port' : mysql.port(),
        'gdb_dbname' : mysql.databasename(),
        'gdb_user' : mysql.user(),
        'gdb_password' : mysql.password(),
    })
    status_set('maintenance', 'Rendering config file')
    set_flag('endpoint.database.connected')
    set_flag('restart-app')

@when('restart-app')
def restart_app():
    host.service_reload('apache2')
    clear_flag('restart-app')
    status_set('active', 'App ready')
