#!/bin/sh

FLASK_ENV=development DUSTPATH_SETTINGS=$(pwd)/dustpath-development.cfg DEBUG=1 dustpath-web -d
