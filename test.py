#!/usr/bin/env python

import nose
import os

from services import system

os.environ['APP_ENVIRONMENT'] = 'testing'
args = ['tests', '--with-spec', '--spec-color', '--nologcapture']

system.connect_mongo()

nose.run(argv=args)