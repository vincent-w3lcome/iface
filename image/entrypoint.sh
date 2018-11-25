#!/bin/bash

source /usr/src/yuwenmao/iface/venv/bin/activate

uwsgi --ini /usr/src/yuwenmao/iface/conf/uwsgi.ini
