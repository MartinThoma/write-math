#!/usr/bin/env python

"""A simple web server that listens on http://localhost:8080/."""

import web

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())


class hello:
    def GET(self, name):
        get_paramters = web.input()

        if 'heartbeat' in get_paramters:
            return get_paramters['heartbeat']

        return 'stadard return (get)'

    def POST(self, name):
        get_paramters = web.input()

        if 'heartbeat' in get_paramters:
            return get_paramters['heartbeat']

        if 'classify' in get_paramters:
            return str(get_paramters)

        return 'stadard return (post)'

if __name__ == "__main__":
    app.run()
