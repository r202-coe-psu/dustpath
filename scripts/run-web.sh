#!/bin/sh

FLASK_ENV=development MYAPP_SETTINGS=$(pwd)/dustpath.cfg DEBUG=1 dustpath-web -d
