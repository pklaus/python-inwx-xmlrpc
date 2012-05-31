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

##########################################################################
######   This is an example of how to use the inwx class to back   #######
######   up all your DNS entries via the InterNetworX XMLRPC API.  #######

from inwx import domrobot
from configuration import get_account_data, get_nsbackup_files

def main():
    api_url, username, password = get_account_data(True)
    backup_files = get_nsbackup_files(True)
    if 'pickle_backup_file' in backup_files.keys():
        from pickle import Pickler
    if 'json_backup_file' in backup_files.keys():
        import json
    # Instantiate the inwx class (does not connect yet but dispatches calls to domrobot objects with the correct API URL
    inwx_conn = domrobot(api_url, username, password, 'en', False)
    # get the list of all domains:
    domains = inwx_conn.nameserver.list()['domains']
    # get all the nameserver entries for each domain
    current, total = 0, len(domains)
    nsentries = dict()
    for domain in domains:
        current += 1
        domain = domain['domain']
        print "%i of %i - Currently backing up %s." % (current, total, domain)
        nsentries[domain] = inwx_conn.nameserver.info({'domain': domain})['record']
    if 'pickle_backup_file' in backup_files.keys():
        Pickler(open(backup_files['pickle_backup_file'],'wb')).dump(nsentries)
        print "Wrote backup file using Python Module Pickle : %s." % backup_files['pickle_backup_file']
    if 'json_backup_file' in backup_files.keys():
        json.dump(nsentries, open(backup_files['json_backup_file'], 'w'))
        print "Wrote backup file using Python Module JSON: %s." % backup_files['json_backup_file']

if __name__ == '__main__':
    main()
