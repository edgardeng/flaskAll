"""
@date: 2020-09-01
@author: edgardeng

-- demo for flask with celery (flask-1.1.2 ,celery-4.4.7 ,redis-3.5.3 )

"""
import random
import time
from flask import Flask, request, render_template, session, flash, redirect,url_for, jsonify
# from flask_mail import Mail, Message
from celery import Celery


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Flask-Mail configuration
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = 'flask@example.com'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/3'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/4'


# Initialize extensions
# mail = Mail(app)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def send_async_email(email_data):
  """Background task to send an email with Flask-Mail."""
  print('send_async_email', email_data)
  time.sleep(random.randint(0, 3))
  print('send_async_email ok')
  # msg = Message(email_data['subject'],
  #               sender=app.config['MAIL_DEFAULT_SENDER'],
  #               recipients=[email_data['to']])
  # msg.body = email_data['body']
  # with app.app_context():
  #   mail.send(msg)


@celery.task(bind=True)
def long_task(self):
  """Background task that runs a long function with progress reports."""
  verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
  adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
  noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
  message = ''
  total = random.randint(10, 50)
  for i in range(total):
    if not message or random.random() < 0.25:
      message = '{0} {1} {2}...'.format(random.choice(verb),
                                        random.choice(adjective),
                                        random.choice(noun))
    self.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': message})
    time.sleep(0.2)
  return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42}


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html', email=session.get('email', ''))
  email = request.form['email']
  session['email'] = email

  # send the email
  email_data = {
    'subject': 'Hello from Flask',
    'to': email,
    'body': 'This is a test email sent from a background Celery task.'
  }
  if request.form['submit'] == 'Send':
    send_async_email.delay(email_data)          #  send right away
    flash('Sending email to {0}'.format(email))
  else:
    send_async_email.apply_async(args=[email_data], countdown=60) # send in one minute
    flash('An email will be sent to {0} in one minute'.format(email))
  return redirect(url_for('index'))


@app.route('/create_task', methods=['POST'])
def create_task():
  task = long_task.apply_async()
  # 202状态码适合异步任务或者说需要处理时间比较长的请求，避免HTTP连接一直占用，超时这些情况。常见的就是使用MQ异步处理批任务，客户端定时轮训结果。
  return jsonify({}), 202, {'Location': url_for('task_status', task_id=task.id)}


@app.route('/status/<task_id>')
def task_status(task_id):
  task = long_task.AsyncResult(task_id) # 通过id 获取异步结果
  if task.state == 'PENDING':
    response = {
      'state': task.state,
      'current': 0,
      'total': 1,
      'status': 'Pending...'
    }
  elif task.state != 'FAILURE':
    response = {
      'state': task.state,
      'current': task.info.get('current', 0),
      'total': task.info.get('total', 1),
      'status': task.info.get('status', '')
    }
    if 'result' in task.info:
      response['result'] = task.info['result']
  else:
    # something went wrong in the background job
    response = {
      'state': task.state,
      'current': 1,
      'total': 1,
      'status': str(task.info),  # this is the exception raised
    }
  return jsonify(response)


'''
'   Start Steps:
    1. run redis at 6396
    2. run celery ` celery worker -A index.celery -l info`
    3. run flask app 
'''
if __name__ == '__main__':
  app.run(debug=True)

