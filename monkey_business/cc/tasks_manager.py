import os
import time
from flask import Flask
from flask.ext.pymongo import PyMongo
from celery import Celery

def make_celery(app):
    celery = Celery(main='MONKEY_TASKS', backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

fapp = Flask(__name__)
fapp.config.from_object('dbconfig')
celery = make_celery(fapp)
mongo = PyMongo(fapp)

@celery.task
def run_task(jobid):
    task_id = run_task.request.id
    print "searching for ", jobid
    job = mongo.db.job.find_one({"_id": jobid})
    if not job:
        return False
    job["execution"]["state"] = "processing"
    mongo.db.job.update({"_id": jobid}, job)

    time.sleep(30)

    job["execution"]["state"] = "done"
    mongo.db.job.update({"_id": jobid}, job)
    return "task: " + task_id


@celery.task
def update_cache(connector):
    time.sleep(30)
    return "job: " + repr(job)
