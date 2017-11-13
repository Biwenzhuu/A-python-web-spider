
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def application (environ, start_resopnse):
    start_resopnse('200 OK',[('Content_Type', 'text/html')])
    body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
    return [body.encode('utf-8')]
