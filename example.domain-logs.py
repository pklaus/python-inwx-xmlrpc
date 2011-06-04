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

from inwx import inwx, prettyprint
from configuration import get_account_data
import json

def main():
    api_url, username, password, secure = get_account_data(True)
    inwx_conn = inwx(api_url, username, password, 'en', secure, False)
    print prettyprint.domains(inwx_conn.nameserver.list()['domains'])
    # get the list of all domains:
    domains = inwx_conn.nameserver.list()['domains']
    for domain in domains:
        domain = domain['domain']
        print "Logs for domain %s:" % domain
        print prettyprint.domain_log(inwx_conn.domain.log({'domain': domain})['domain'])

if __name__ == '__main__':
    main()