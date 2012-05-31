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
    print prettyprint.domains(inwx_conn.nameserver.list()['domains'])

if __name__ == '__main__':
    main()
