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
######   This is an example of how to use the inwx class to   #######
######   update a DNS entry via the InterNetworX XMLRPC API.  #######

from inwx import inwx
from configuration import get_account_data, get_domain_update

def main():
    api_url, username, password, secure = get_account_data(True)
    domain, subdomain, new_ip = get_domain_update(True)
    # Instantiate the inwx class (does not connect yet but dispatches calls to domrobot objects with the correct API URL
    inwx_conn = inwx(api_url, username, password, 'en', secure, False)
    # get all the nameserver entries for a certain domain 
    nsentries = inwx_conn.nameserver.info({'domain': domain})
    for record in nsentries['record']:
        if subdomain == record['name']:
            id = record['id']
            break
    if id:
        inwx_conn.nameserver.updateRecord({'id':id,'content':new_ip,'ttl':3600})
    else:
        print "Subdomain not in list of nameserver entries."

if __name__ == '__main__':
    main()
