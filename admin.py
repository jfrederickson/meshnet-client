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
import os
from error import ErrorWindow

class AdminInterface:
    admin = None
    conf = None
    cjdns = None
    adminpath = os.getenv("HOME") + '/.cjdnsadmin'
    
    def __init__(self):
        # Load .cjdnsadmin
        f = open(self.adminpath)
        self.admin = json.loads(f.read())
        adminpass = self.admin['password']
        adminport = int(self.admin['port'])
        f.close()
        
        # Load cjdroute.conf
        f = open(self.admin['config'])
        try:
            self.conf = json.loads(f.read())
            # Only connect to cjdns if we can read the config file.
            # We really could connect here, but then we couldn't update
            # cjdroute.conf so let's not confuse the user. 
            self.cjdns = connect(self.admin['addr'], adminport, adminpass)
        except ValueError:
            raise IOError
        f.close()
        
    def functions(self, cjdns):
        cjdns.functions()
        routes = cjdns.NodeStore_dumpTable(0)
        print(routes)
    def save(self):
        f = open(self.confpath, 'w')
        f.write(json.dumps(self.conf, sort_keys=True, indent=4))
        f.close()
    def addPeer(self, key, pw, v4, port):
        try:
            socket.inet_aton(v4)
            if(int(port) >= 0 and int(port) <= 65535):
                ip = v4+':'+port
                peer = dict([(ip, dict([('password', pw), ('publicKey', key)]))])
                
                self.cjdns.UDPInterface_beginConnection(1, pw, key, ip)
                return True
            else:
                return 'Invalid Port' # TODO: Actual error handling (learning more python)
        except socket.error:
            return 'Invalid IP address'