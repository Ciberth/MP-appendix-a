#!/usr/bin/python

import pwd
import os
from subprocess import call
from charmhelpers.core import host
from charmhelpers.core.hookenv import log, status_set, config
from charmhelpers.core.templating import render
from charms.reactive import when, when_not, set_flag, clear_flag, when_file_changed, endpoint_from_flag
from charms.reactive import Endpoint


################################################
#                                              #
# Apache stuff                                 #
#                                              #
################################################


@when('apache.available')
def finishing_up_setting_up_sites():
    host.service_reload('apache2')
    set_flag('apache.start')

@when('apache.start')
def ready():
    host.service_reload('apache2')
    status_set('active', 'apache ready - gdb not concrete')

###############################################
#
# Mysql support
#
###############################################

@when('mysql.connected', 'endpoint.proxy.mysql.requested')
def request_mysql_db():
    db_request_endpoint = endpoint_from_flag('endpoint.proxy.mysql.requested')

    databasename = db_request_endpoint['databasename']
    username = db_request_endpoint['username']

    mysql_endpoint = endpoint_from_flag('mysql.connected')
    mysql_endpoint.configure(databasename, username, prefix="gdb")

    status_set('maintenance', 'Requesting mysql db')


@when('mysql.available', 'endpoint.proxy.mysql.requested')
def render_mysql_config_and_share_details():  
 
    mysql_endpoint = endpoint_from_flag('mysql.available')

    # On own apache
    render('gdb-config.j2', '/var/www/generic-database/gdb-config.html', {
        'db_master': "no-master",
        'db_pass': mysql_endpoint.password("gdb"),
        'db_dbname': mysql_endpoint.database("gdb"),
        'db_host': mysql_endpoint.db_host(),
        'db_user': mysql_endpoint.username("gdb"),
        'db_port': "3306",
    })

    # share details to consumer-app
    gdb_endpoint = endpoint_from_flag('endpoint.proxy.mysql.requested')
    
    gdb_endpoint.share_details(
        "mysql",
        mysql_endpoint.db_host(),
        mysql_endpoint.database("gdb"),
        mysql_endpoint.username("gdb"),
        mysql_endpoint.password("gdb"),
        "3306",
    )
    
    clear_flag('endpoint.proxy.mysql.requested')
    set_flag('endpoint.proxy.mysql.available')
    set_flag('endpoint.proxy.concrete')
    set_flag('restart-app')



@when('restart-app')
def restart_app():
    host.service_reload('apache2')
    clear_flag('restart-app')
    status_set('active', 'Apache/gdb ready and concrete')

