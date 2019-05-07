from mongoengine import Document, DateTimeField


class MonkeyTtl(Document):
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
