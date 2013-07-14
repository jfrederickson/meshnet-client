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
                
                self.cjdns.UDPInterface_beginConnection(0, pw, key, ip)
                return True
            else:
                return 'Invalid Port' # TODO: Actual error handling (learning more python)
        except socket.error:
            return 'Invalid IP address'