#!/usr/bin/env python
#
# Delete all pyc files in the local directory. Python doesn't seem to always
# refresh these correctly when the source code has changed, so to be on the
# safe side we run this when updating the source tree. 
#

import os

for root, dirs, files in os.walk(os.path.abspath(os.path.dirname(__file__))):
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == '.pyc':
            os.unlink(os.path.join(root, file))
