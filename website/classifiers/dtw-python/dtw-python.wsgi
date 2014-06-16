#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/dtw-python/")

from index import app as application
application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTsss'