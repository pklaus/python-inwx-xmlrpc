#!/usr/bin/env python
# -*- encoding: UTF8 -*-

# authors: L3viathan, github.com/L3viathan
#          Philipp Klaus, philipp.klaus →AT→ gmail.com

# This file is part of inwx-dyndns
#
# inwx-dyndns is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# inwx-dyndns is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with inwx-dyndns. If not, see <http://www.gnu.org/licenses/>.

# This is obviously heavily borrowed (almost everything is the same) from Philipp Klaus' python-inwx-xmlrpc.

from inwx import domrobot
from configuration import get_account_data, get_domain_update
from urllib2 import urlopen

IPV4_DETECTION_API = 'http://ip.42.pl/raw'

def main():
    api_url, username, password = get_account_data(True)
    domain, subdomain, default_ip = get_domain_update(True)
    try:
        new_ip = urlopen(IPV4_DETECTION_API).read()
    except:
        # If something failed with the IPv6 detection, we may abort at this point
        return
        # or simply set the default value:
        new_ip = default_ip
    # Instantiate the inwx class (does not connect yet but dispatches calls to domrobot objects with the correct API URL
    inwx_conn = domrobot(api_url, username, password, 'en', False)
    # get all the nameserver entries for a certain domain 
    nsentries = inwx_conn.nameserver.info({'domain': domain})
    for record in nsentries['record']:
        if subdomain == record['name']:
            id = record['id']
            break
    if id:
        print "Setting subdomain %s to the new IPv4 IP %s." % (subdomain, new_ip)
        inwx_conn.nameserver.updateRecord({'id':id,'content':new_ip,'ttl':3600})
    else:
        print "Subdomain not in list of nameserver entries."

if __name__ == '__main__':
    main()
