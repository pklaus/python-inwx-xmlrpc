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
######   This the most important file of the project:         #######
######   It contains the classes inwx and domrobot, which     #######
######   implement the XML-RPC communication with the         #######
######   InterNetworX API.                                    #######

from time import time
from xmlrpclib import ServerProxy, Fault, ProtocolError, _Method
from hashlib import sha256

VALID_OBJECTNAMES = ['contact', 'domain', 'nameserver', 'nameserverset', 'accounting', 'host', 'pdf', 'message', 'application']

class domrobot (ServerProxy):
    def __init__ (self, address, username=False, password=False, language='en', secure=True, verbose=False):
        self.__address = address
        self.__username = username
        self.__password = password
        self.__language = language
        self.__secure = secure
        #super(domrobot, self).__init__(address, verbose=debug)
        ServerProxy.__init__(self, address,verbose=verbose)
   
    def __getattr__(self,name):
        return _Method(self.__request, name)
 
    def __request (self, methodname, params):
        self.__params = dict()
        self.__params['user'] = self.__username
        self.__params['lang'] = self.__language
        if self.__secure: # transmit password in secure-mode
            nonce = time()
            self.__params['pass']=sha256(str(nonce)+self.__password).hexdigest() # sha256 hash of the nonce and the password
            self.__params['nonce']=nonce
        else:
            self.__params['pass'] = self.__password
        if len(params)>0 and type(params[0]) is dict: self.__params.update(params[0])
        method_function = ServerProxy.__getattr__(self,methodname)
        try:
            response = method_function(self.__params)
        except Fault, err:
            raise NameError("Fault", err)
        except ProtocolError, err:
            raise NameError("ProtocolError", err)
        except Exception, err:
            raise NameError("Some other error occured, presumably with the network connection to %s" % self.__address, err)
        if response['msg'] == 'Command completed successfully' or response['code'] == 1000:
            try:
                return response['resData']
            except:
                # not all requests send a response
                return None
        else:
            raise NameError('There was a problem: %s (Error code %s)' % (response['msg'], response['code']), response)

# The inwx class enables easy access to the objects of the InterNetworX XML-RPC API.
class inwx (object):
    def __init__ (self, address, username=False, password=False, language='en', secure=True, verbose=False):
        self.__address = address
        self.__username = username
        self.__password = password
        self.__language = language
        self.__secure = secure
        self.__verbose = verbose
        self.__robots = dict()
    # The main use of this class is to dispatch calls to domrobot instances (each having its own API URL):
    def __getattr__(self,name):
        if name in VALID_OBJECTNAMES:
            if name not in self.__robots.keys():
                self.__robots[name] = domrobot(self.__address+'/'+name, self.__username, self.__password, self.__language, self.__secure, self.__verbose)
            return self.__robots[name]
