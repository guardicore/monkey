from datetime import datetime, timedelta

from mongoengine import Document, DateTimeField


class MonkeyTtl(Document):
    """
    This model represents the monkey's TTL, and is referenced by the main Monkey document.
    See https://docs.mongodb.com/manual/tutorial/expire-data/ and
    https://stackoverflow.com/questions/55994379/mongodb-ttl-index-doesnt-delete-expired-documents/56021663#56021663
    for more information about how TTL indexing works and why this class is set up the way it is.
    """

    def __init__(self, expiry_in_seconds, *args, **values):
        """
        Initializes a TTL object which will expire in expire_in_seconds seconds from when created.
        Remember to call .save() on the object after creation.
        :param expiry_in_seconds: How long should the TTL be in the DB, in seconds. Please take into consideration
        that the cleanup thread of mongo might take extra time to delete the TTL from the DB.
        """
        # Using UTC to make the mongodb TTL feature work. See
        # https://stackoverflow.com/questions/55994379/mongodb-ttl-index-doesnt-delete-expired-documents.
        super(MonkeyTtl, self).__init__(
            expire_at=datetime.utcnow() + timedelta(seconds=expiry_in_seconds), *args, **values)

    meta = {
        'indexes': [
            {
                'name': 'TTL_index',
                'fields': ['expire_at'],
                'expireAfterSeconds': 0
            }
        ]
    }

    expire_at = DateTimeField()
