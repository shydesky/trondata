#!/usr/bin/env bash

#export LC_ALL=C.UTF-8
#export LANG=C.UTF-8
export COLOREDLOGS_LOG_FORMAT='%(asctime)s %(hostname)s %(name)s[%(funcName)s]-%(levelname)s Line:%(lineno)s  %(message)s'

export FLASK_APP='./autoapp.py'
export FLASK_DEBUG=1
export USE_CONFIG='dev'
flask run -h0.0.0.0 -p1300
