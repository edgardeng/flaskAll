#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2019-06-21
@author: edgardeng

-- demo for flask scheduler

"""

from flask import Flask
from flask_apscheduler import APScheduler
from flask_apscheduler.auth import HTTPBasicAuth
import datetime


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'index:test_task',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 3
        }
    ]
    SCHEDULER_API_ENABLED = True
    SCHEDULER_AUTH = HTTPBasicAuth()
    # SCHEDULER_ALLOWED_HOSTS = ['my_servers_name']


def test_task(a, b):
    print(str(a) + ' ' + str(b), datetime.datetime.now())


app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
# it is also possible to enable the API directly
# scheduler.api_enabled = True
# scheduler.auth = HTTPBasicAuth()
# scheduler.allowed_hosts = ['my_servers_name']
scheduler.init_app(app)


@scheduler.authenticate
def authenticate(auth):
    return auth['username'] == 'guest' and auth['password'] == 'guest'


if __name__ == '__main__':
    scheduler.start()
    app.run()
