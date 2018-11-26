#!/bin/bash

source /usr/src/yuwenmao/iface/venv/bin/activate

cd /usr/src/yuwenmao/iface/ && export LANG=en_US.UTF-8; uwsgi --ini ./conf/uwsgi.ini
