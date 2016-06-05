SRV_ADDRESS = 'localhost:27017'
BROKER_URL = 'mongodb://%(srv)s/monkeybusiness' % {'srv': SRV_ADDRESS}
MONGO_URI = BROKER_URL
CELERY_RESULT_BACKEND = 'mongodb://%(srv)s/' % {'srv': SRV_ADDRESS}
CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'monkeybusiness',
    'taskmeta_collection': 'celery_taskmeta',
}
#CELERYD_LOG_FILE="../celery.log"