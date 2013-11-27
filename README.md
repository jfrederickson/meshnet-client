meshnet-client
==============

A GUI client (PyQt) for cjdns.  It's a work in progress, currently only adding peers works.

#Dependencies

- PyQt4
- cjdns python API

#Running

####Warning: Back up your cjdroute.conf before running!

Ensure that your cjdroute.conf is writable by your user account and that you have a .cjdnsadmin file in your home directory.  (This client will not create one for you as of now, create one with another utility such as [cjdcmd](https://github.com/inhies/cjdcmd).)

Add the contrib/python directory in your cjdns installation directory to your PYTHONPATH.  If cjdns is installed in /opt/cjdns, you can do this temporarily by running:

    export PYTHONPATH=$PYTHONPATH:/opt/cjdns/contrib/python

Run the client with ```python2 gui.py```.
