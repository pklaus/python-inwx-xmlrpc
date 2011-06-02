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

#############################################################################
######   This is an example of how to use the inwx class to back      #######
######   download all your invoices via the InterNetworX XMLRPC API.  #######

from inwx import inwx
from configuration import get_account_data, get_invoices_folder
from os.path import isfile

def main():
    api_url, username, password, secure = get_account_data(True)
    invoices_folder = get_invoices_folder(True)
    # Instantiate the inwx class (does not connect yet but dispatches calls to domrobot objects with the correct API URL
    inwx_conn = inwx(api_url, username, password, 'en', secure, False)
    # get the list of all invoices up to now
    invoices = inwx_conn.accounting.listInvoices()
    # download each invoice (if not already downloaded)
    current, total = 0, invoices['count']
    if total > 0: print "Saving the %i invoices to %s" % (total, invoices_folder)
    for invoice in invoices['invoice']:
        current += 1
        id = invoice['invoiceId']
        date = invoice['date']
        amount_after_tax = invoice['afterTax']
        amount_before_tax = invoice['preTax']
        type = invoice['type']
        filename = "%s_%.2f_%s.pdf" % (date, amount_before_tax, id)
        full_path = invoices_folder + '/' + filename
        if isfile(full_path):
            print "%i of %i - Invoice %s (%s) already downloaded and saved to %s" % (current, total, id, date, filename)
        else:
            print "%i of %i - Currently fetching invoice %s (%s) and saving to %s..." % (current, total, id, date, filename)
            invoice_data = inwx_conn.accounting.getInvoice({'invoiceid': id})
            with open(full_path, "wb") as handle:
                handle.write(invoice_data['pdf'].data)

if __name__ == '__main__':
    main()
