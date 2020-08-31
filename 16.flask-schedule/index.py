#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2019-06-21
@author: edgardeng

-- demo for flask scheduler (flask-1.1.2 , flask-apscheduler-1.11.0  )

"""

from flask import Flask, render_template, jsonify, redirect, request
from flask_apscheduler import APScheduler
import datetime
import uuid


class Config(object):
    JOBS = [
        # {
        #     'id': 'job1',
        #     'func': 'index:test_task',
        #     'args': (1, 2),
        #     'trigger': 'interval',
        #     'seconds': 3
        # }
    ]
    SCHEDULER_API_ENABLED = True


def task_one_param(a):
    print('task_one_param', str(a), datetime.datetime.now())


def task_two_param(a, b):
    print('task_two_param', str(a) + ' - ' + str(b), datetime.datetime.now())


def task_no_param():
    print('task_no_param', datetime.datetime.now())


app = Flask(__name__)
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler_jobs = []
scheduler_func = ['index:task_one_param', 'index:task_two_param', 'index:task_no_param']


@app.route('/')
def index():
    return render_template('index.html', funcs=scheduler_func, jobs=scheduler_jobs)


@app.route('/', methods=['POST'])
def scheduler_add():
    if not request.json or 'func' not in request.json:
        return jsonify({'msg': 'no form data'})
    print(type(request.json), request.json)
    job = request.json
    # add_interval_task(func=job['func'], seconds=int(job['seconds']), param=job['param'])
    add_cron_task(func=job['func'], seconds=job['seconds'], param=job['param'])
    return render_template('index.html', funcs=scheduler_func, jobs=scheduler_jobs)


@app.route('/scheduler/pause/<id>')
def scheduler_pause(id):
    pause_task(id)
    return redirect('/')


@app.route('/scheduler/resume/<id>')
def scheduler_resume(id):
    resume_task(id)
    return redirect('/')


@app.route('/scheduler/delete/<id>')
def scheduler_delete(id):
    delete_task(id)
    return redirect('/')


def dict_job(kwargs):
    id = str(uuid.uuid1())[:8]
    job = {
        'id': id,
        'func': kwargs['func'],
        'seconds': kwargs['seconds']
    }
    if 'param' in kwargs:
        job['args'] = kwargs['param']
    if 'task_two_param' in job['func']:
        job['args'] = tuple(job['args'])
    return job  # change http json param to scheduler JOB


def add_interval_task(**kwargs):
    job = dict_job(kwargs)
    try:
        result = scheduler.add_job(func=job['func'],
                                   id=job['id'],
                                   trigger='interval',
                                   args=job['args'],
                                   seconds=int(job['seconds']))
        job['status'] = 'running'
        job['trigger'] = 'interval'
        scheduler_jobs.append(job)
    except ValueError as e:
        print(e)


def add_cron_task(**kwargs):
    job = dict_job(kwargs)
    try:
        result = scheduler.add_job(func=job['func'],
                                   id=job['id'],
                                   trigger='cron',
                                   args=job['args'],
                                   second=job['seconds'])
        job['status'] = 'running'
        job['trigger'] = 'cron'
        scheduler_jobs.append(job)
    except ValueError as e:
        print(e)


def pause_task(id):
    scheduler.pause_job(id)
    for job in scheduler_jobs:
        if job['id'] == id:
            job['status'] = 'paused'
            break


def resume_task(id):
    scheduler.resume_job(id)
    for job in scheduler_jobs:
        if job['id'] == id:
            job['status'] = 'running'
            break


def delete_task(id):
    result = scheduler.remove_job(id)
    for job in scheduler_jobs:
        if job['id'] == id:
            scheduler_jobs.remove(job)
            break


if __name__ == '__main__':
    scheduler.start()
    add_interval_task(func='index:task_two_param', param=(1, 2), seconds=3)  # start a interval task when app started
    app.run()
