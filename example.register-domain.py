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

###########################################################################
#######    This is an example of how to use the inwx class to      ########
#######    list all your domains via the InterNetworX XMLRPC API.  ########

from inwx import domrobot, prettyprint
from configuration import get_account_data

def main():
    api_url, username, password = get_account_data(True)
    inwx_conn = domrobot(api_url, username, password, 'en', False)
    print prettyprint.contacts(inwx_conn.contact.list()['contact'])
    print prettyprint.nameserversets(inwx_conn.nameserverset.list()['nsset'])
    print "\nRegister a new domain\n"
    domainname = raw_input('New Domain [e.g. example.com]: ')
    check = inwx_conn.domain.check({'domain': domainname})
    if check['domain'][0]['status'] == 'free':
        if raw_input("The domain %s is available. Do you want to register now? [yes/no]: " % domainname) != 'yes': return
        registrant_id = int(raw_input('Please give the ID for the registrant and admin contact [e.g. 1023532]: '))
        admin_id = registrant_id
        tech_id, billing_id = 1,1
        nameservers = ['ns.inwx.de','ns2.inwx.de','ns3.inwx.de']
        reg_result = inwx_conn.domain.create({'domain':domainname, 'registrant': registrant_id, 'admin': admin_id, 'tech': tech_id, 'billing': billing_id, 'ns': nameservers})
        if reg_result == None:
            print "Successfully registered the domain."
    else:
        print "Sorry, the domain %s is not available anymore." % domainname
        print "The current status of the domain is '%s'." % check['domain'][0]['status']

if __name__ == '__main__':
    main()
