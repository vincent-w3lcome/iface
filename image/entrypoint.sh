#!/bin/bash

source /yuwenmao/iface/venv/bin/activate

cd /yuwenmao/iface/ && export LANG=en_US.UTF-8; uwsgi --ini ../uwsgi.ini
