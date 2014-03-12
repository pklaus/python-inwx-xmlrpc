#!/usr/bin/env python2.7
# -*- encoding: UTF8 -*-

# author: Philipp Klaus, philipp.klaus →AT→ gmail.com
# author: Markus Roth,   mail →AT→ rothmark.us

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

from inwx import domrobot
from configuration import get_account_data, get_domain_update
from urllib import urlopen

# Mapping from type to webservice for external IP determination
record_type_to_api = {
    'A':    'http://v4.ipv6-test.com/api/myip.php',
    'AAAA': 'http://v6.ipv6-test.com/api/myip.php'
}

# Call webservice to obtain external IP
def get_ip(api):
    try:
        ip = urlopen(api).read().decode('ascii')
        return ip
    except:
        return None

def main():
    api_url, username, password = get_account_data(True)
    domain, subdomain, _ = get_domain_update(True)

    # Instantiate the inwx class (does not connect yet but dispatches calls to domrobot objects with the correct API URL
    inwx_conn = domrobot(api_url, username, password, 'en', False)
    nsentries = inwx_conn.nameserver.info({'domain': domain})

    # Filter entries for subdomain
    nsentries = [record for record in nsentries['record'] if subdomain == record['name']]

    assert nsentries, "Subdomain %s not in list of nameserver entries." % subdomain

    # There may be multiple entries for one subdomain, one for each type (A, AAAA, ...)
    for record in nsentries:
        record_type = record['type'] # A, AAAA
        assert record_type in record_type_to_api, "Unsupported record type: %s" % record_type
        
        new_ip = get_ip(record_type_to_api[record_type])
        if new_ip:
            print "Updating %s record of %s from %s to %s" % (record_type, record['name'], record['content'], new_ip)
            inwx_conn.nameserver.updateRecord({'id': record['id'], 'content': new_ip, 'ttl': 3600})
            
if __name__ == '__main__':
    main()
