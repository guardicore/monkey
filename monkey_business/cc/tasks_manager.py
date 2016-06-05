import time
from flask import Flask
from datetime import datetime
from flask.ext.pymongo import PyMongo
from celery import Celery
from common import *

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

class JobExecution(object):
    _jobinfo = None
    _job = None
    _mongo = None
    _log = []

    def __init__(self, mongo, jobinfo):
        self._mongo = mongo
        self._jobinfo = jobinfo
        self.update_job_state("processing")

        job_class = get_jobclass_by_name(self._jobinfo["type"])
        con = job_class.connector()
        refresh_connector_config(self._mongo, con)
        self._job = job_class(con)

    def get_job(self):
        return self._job

    def refresh_job_info(self):
        self._jobinfo = self._mongo.db.job.find_one({"_id": self._jobinfo["_id"]})

    def update_job_state(self, state):
        self._jobinfo["execution"]["state"] = state
        self._mongo.db.job.update({"_id": self._jobinfo["_id"]},
                                  {"$set": {"execution": self._jobinfo["execution"]}})

    def _log_resutls(self, res):
        self._mongo.db.results.update({"jobid": self._jobinfo["_id"]},
                                      {"$set": {"results": {"time" : datetime.now(), "res" : res}}},
                                      upsert=True)

    def log(self, text):
        self._log.append("[%s] %s" % (datetime.now(), text))
        self._mongo.db.results.update({"jobid": self._jobinfo["_id"]},
                                      {"$set": {"log": self._log}},
                                      upsert=True)

    def run(self):
        self.log("Starting job")
        try:
            self._job.run()
        except Exception, e:
            self.log("Exception raised while running: %s" % e)
            self.update_job_state("error")
            return False
        self.log("done job startup")
        self.update_job_state("running")
        return True

    def get_results(self):
        self.log("Trying to get results")
        res = []
        try:
            res = self._job.get_results()
        except Exception, e:
            self.log("Exception raised while getting results: %s" % e)
            return False
        self._log_resutls(res)
        return True


@celery.task
def run_task(jobid):
    print "searching for ", jobid
    job_info = mongo.db.job.find_one({"_id": jobid})
    if not job_info:
        return False

    job_exec = JobExecution(mongo, job_info)
    if not job_exec.get_job():
        job_exec.update_job_state(job_info, "error")
        return False

    if not job_exec.run():
        return False

    if not job_exec.get_results():
        return False

    return "done task: " + run_task.request.id


@celery.task
def update_cache(connector):
    time.sleep(30)
    return "connector: " + repr(connector)
