#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# author: Philipp Klaus, philipp.klaus →AT→ gmail.com

# This file is part of python-inwx-xmlrpc.
#
# python-inwx-xmlrpc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-inwx-xmlrpc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-inwx-xmlrpc. If not, see <http://www.gnu.org/licenses/>.

#####################################################################
######   This file helps to handle the INI-style .cfg files.   ######


import sys
import ConfigParser
from os.path import expanduser

def get_account_data(print_errors = False, config_file = 'python-inwx-xmlrpc.cfg', config_section = 'main_account'):
    """
    boolean print_errors:   Print errors to stdout instead of raising an exception.
    string config_file:     The name of the configuration file.
    string config_section:  The name of the section to read in the configuration file.
    """
    config = open_config_file(print_errors, config_file)
    try:
        api_url = config.get(config_section, 'api_url')
        username = config.get(config_section, 'username')
        password = config.get(config_section, 'password')
        try:
            secure = {'true': True, 'false': False}.get(config.get(config_section, 'secure').lower())
        except:
            secure = True
    except Exception, err:
        message = 'Error: Please make sure your config file %s contains the section %s with the entries "api_url", "username" and "password".' % (config_file, config_section)
        if print_errors:
            print message
            sys.exit(2)
        else:
            raise NameError(message)
    return (api_url, username, password, secure)

def get_domain_update(print_errors=False, config_file = 'python-inwx-xmlrpc.cfg', config_section = 'automatic_nameserver_entry_update'):
    config = open_config_file(print_errors, config_file)
    try:
        domain = config.get(config_section, 'domain')
        subdomain = config.get(config_section, 'subdomain')
        default_ip = config.get(config_section, 'default_ip')
    except Exception, err:
        message = 'Error: Please make sure your config file %s contains the section %s with the entries "domain", "subdomain" and "default_ip".' % (config_file, config_section)
        if print_errors:
            print message
            sys.exit(2)
        else:
            raise NameError(message)
    return domain, subdomain, default_ip

def get_invoices_folder(print_errors=False, config_file = 'python-inwx-xmlrpc.cfg', config_section = 'invoices_folder'):
    config = open_config_file(print_errors, config_file)
    try:
        invoices_folder = expanduser(config.get(config_section, 'invoices_folder'))
    except:
        message = 'Error: Please make sure your config file %s contains the section %s with the entry "invoices_folder".' % (config_file, config_section)
        if print_errors:
            print message
            sys.exit(2)
        else:
            raise NameError(message)
    return invoices_folder


def get_nsbackup_files(print_errors=False, config_file = 'python-inwx-xmlrpc.cfg', config_section = 'nameserver_backup'):
    config = open_config_file(print_errors, config_file)
    backup_files = dict()
    try:
        backup_files['json_backup_file'] = expanduser(config.get(config_section, 'json_backup_file'))
    except:
        pass
    try:
        backup_files['pickle_backup_file'] = expanduser(config.get(config_section, 'pickle_backup_file'))
    except:
        pass
    if len(backup_files) == 0 :
        message = 'Error: Please make sure your config file %s contains the section %s with the entries "json_backup_file" or "pickle_backup_file".' % (config_file, config_section)
        if print_errors:
            print message
            sys.exit(2)
        else:
            raise NameError(message)
    return backup_files

def open_config_file(print_errors, config_file):
    config = ConfigParser.ConfigParser()
    try:
        if config.read(config_file) == []: raise Exception()
    except:
        message = "Error: Please make sure you adopted the config file: %s" % config_file
        if print_errors:
            print message
            sys.exit(2)
        else:
            raise NameError(message)
    return config
