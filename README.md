meshnet-client
==============

A GUI client (PyQt) for cjdns.  It's very much a work in progress and many things are specific to my own configuration, so good luck getting it to run.  (Hints: The JSON parser doesn't like comments, get rid of those.  Change the path to cjdroute.conf, yours will be different.  You might need to change the interface number to 0 in admin.py.  I will fix these eventually!)

#Dependencies

- PyQt4
- cjdns python API
