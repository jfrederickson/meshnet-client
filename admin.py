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

class AdminInterface:
    conf = None
    cjdns = None
    confpath = '/etc/cjdroute-dev.conf' # TODO: Better way of finding this
    
    def __init__(self):
        f = open(self.confpath)
        self.conf = json.loads(f.read())
        adminpass = self.conf['admin']['password']
        adminport = int(((self.conf['admin']['bind']).split(":"))[1])
        self.cjdns = connect('127.0.0.1', adminport, adminpass);
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