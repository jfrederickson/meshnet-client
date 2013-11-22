#===============================================================================
#    Copyright 2013 Jonathan Frederickson
#
#     This file is part of meshnet-client.
# 
#     Meshnet-client is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Meshnet-client is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with meshnet-client.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

from cjdnsadmin.cjdnsadmin import connect
import json
import socket
import sys
import os
from error import ErrorWindow

class AdminInterface:
    admin = None
    conf = None
    cjdns = None
    adminpath = os.path.join(os.getenv("HOME"), '.cjdnsadmin')
    
    def __init__(self):
        # Load .cjdnsadmin
        with open(self.adminpath) as f:
            self.admin = json.loads(f.read())
            adminpass = self.admin['password']
            adminport = int(self.admin['port'])
        
        # Load cjdroute.conf
        with open(self.admin['config']) as f:
            try:
                self.conf = json.loads(f.read())
                # Only connect to cjdns if we can read the config file.
                # We really could connect here, but then we couldn't update
                # cjdroute.conf so let's not confuse the user. 
                self.cjdns = connect(self.admin['addr'], adminport, adminpass)
            except ValueError as e:
                raise e #TODO: Do something better here
        
    def functions(self, cjdns):
        cjdns.functions()
        routes = cjdns.NodeStore_dumpTable(0)
        print(routes)
        
    def __save(self):
        with open(self.admin['config'], 'w') as f:
            f.write(json.dumps(self.conf, sort_keys=True, indent=4))
        
    def addPeer(self, key, pw, v4, port):
        """Adds a peer with the given info and updates config"""
        if(int(port) >= 0 and int(port) <= 65535):
            ip = v4+':'+port
            try:
                if(self.__adminAddPeer(key, pw, ip)):
                    self.__confAddPeer(key, pw, ip)
            except socket.error as e:
                raise e
        else:
            raise ValueError('Invalid port number')
        
    def __adminAddPeer(self, key, pw, ip):
        """Adds a peer through the admin interface"""
        try:
            result = self.cjdns.UDPInterface_beginConnection(key, ip, 0, pw)
            if(result['error'] == 'none'):
                return True
            sys.stderr.write(result + '\n')
            return False
        except socket.error as e:
            return False
            raise e
        
    def __confAddPeer(self, key, pw, ip):
        """Adds a peer to the config file"""
        peer = dict([('password', pw), ('publicKey', key)])
        self.conf['interfaces']['UDPInterface'][0]['connectTo'][ip] = peer
        self.__save()
        
    def addJSON(self, peerstring):
        data = json.loads('{' + peerstring + '}')
        ip = str(data.keys()[0])
        pw = str(data[ip]['password'])
        key = str(data[ip]['publicKey'])
        if(self.__adminAddPeer(key, pw, ip)):
            self.conf['interfaces']['UDPInterface'][0]['connectTo'].update(data)
            self.__save()