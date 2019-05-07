from mongoengine import Document, DateTimeField


class MonkeyTtl(Document):
    """
    This model represents the monkey's TTL, and is referenced by the main Monkey document.
    See https://docs.mongodb.com/manual/tutorial/expire-data/ and
    https://stackoverflow.com/questions/55994379/mongodb-ttl-index-doesnt-delete-expired-documents/56021663#56021663
    for more information about how TTL indexing works.

    When initializing this object, do it like so:
    t = MonkeyTtl(expire_at=datetime.utcnow() + timedelta(seconds=XXX))
    """
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
