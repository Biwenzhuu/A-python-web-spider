
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server
from client import application
httpd =make_server('', 8000, application)
print('Serving HTTP on port 80000...')
httpd.serve_forever()
