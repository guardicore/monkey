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

        job_class = get_jobclass_by_name(self._jobinfo["type"])
        con = job_class.connector_type()
        refresh_connector_config(self._mongo, con)
        self._job = job_class(con, self)
        self._job.load_job_properties(self._jobinfo["properties"])
        prev_log = self._mongo.db.results.find_one({"jobid": self._jobinfo["_id"]})
        if prev_log:
            self._log = prev_log["log"]
        else:
            self._log = []

    def get_job(self):
        return self._job

    def refresh_job_info(self):
        self._jobinfo = self._mongo.db.job.find_one({"_id": self._jobinfo["_id"]})

    def update_job_state(self, state):
        self._mongo.db.job.update({"_id": self._jobinfo["_id"]},
                                  {"$set": {"state": state}})

    def _log_resutls(self, res):
        self._mongo.db.results.update({"jobid": self._jobinfo["_id"]},
                                      {"$set": {"results": {"time" : datetime.now(), "res" : res}}},
                                      upsert=True)

    def log(self, text):
        self._log.append([datetime.now().isoformat(), text])
        self._mongo.db.results.update({"jobid": self._jobinfo["_id"]},
                                      {"$set": {"log": self._log}},
                                      upsert=True)

    def run(self):
        self.log("Starting job")

        res = None
        try:
            res = self._job.run()
        except Exception, e:
            self.log("Exception raised while running: %s" % e)
            self.update_job_state("error")
            return False

        if res:
            self.log("Done job startup")
            self.update_job_state("running")
        else:
            self.log("Job startup error")
            self.update_job_state("error")
        return res

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

    def stop(self):
        self.log("Trying to stop...")
        res = None

        try:
            res = self._job.stop()
        except Exception, e:
            self.log("Exception raised while running: %s" % e)
            self.update_job_state("error")
            return False

        if res:
            self.log("Done stop job")
            self.update_job_state("ended")
        else:
            self.log("Job stopping error")
            self.update_job_state("error")

        return res


@celery.task
def run_task(jobid):
    acquire_task = mongo.db.job.update({"_id": jobid, "state": "pending"}, {"$set": {"state": "processing"}})
    if acquire_task["nModified"] != 1:
        return False

    job_info = mongo.db.job.find_one({"_id": jobid})
    if not job_info:
        return False

    job_exec = None
    try:
        job_exec = JobExecution(mongo, job_info)
    except Exception, e:
        print "init JobExecution exception - ", e
        return False

    if not job_exec.get_job():
        job_exec.update_job_state("error")
        return False

    if not job_exec.run():
        return False

    if not job_exec.get_results():
        return False

    return "done task: " + run_task.request.id


@celery.task
def stop_task(jobid):
    acquire_task = mongo.db.job.update({"_id": jobid, "state": "running"}, {"$set": {"state": "stopping"}})
    if acquire_task["nModified"] != 1:
        print "could not acquire lock on job"
        return False

    job_info = mongo.db.job.find_one({"_id": jobid})
    if not job_info:
        print "could not get job info"
        return False

    job_exec = None
    try:
        job_exec = JobExecution(mongo, job_info)
    except Exception, e:
        print "init JobExecution exception - ", e
        return False

    if not job_exec.get_job():
        job_exec.update_job_state("error")
        return False

    job_exec.get_results()

    if not job_exec.stop():
        print "error stopping"
        return False

    return "done stop_task"


@celery.task
def update_cache(connector):
    time.sleep(30)
    return "connector: " + repr(connector)
