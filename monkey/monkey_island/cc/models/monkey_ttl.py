from datetime import datetime, timedelta

from mongoengine import DateTimeField, Document


class MonkeyTtl(Document):
    """
    This model represents the monkey's TTL, and is referenced by the main Monkey document.
    See https://docs.mongodb.com/manual/tutorial/expire-data/ and
    https://stackoverflow.com/questions/55994379/mongodb-ttl-index-doesnt-delete-expired-documents/56021663#56021663
    for more information about how TTL indexing works and why this class is set up the way it is.

    If you wish to use this class, you can create it using the create_ttl_expire_in(seconds) function.
    If you wish to create an instance of this class directly, see the inner implementation of
    create_ttl_expire_in(seconds) to see how to do so.
    """

    @staticmethod
    def create_ttl_expire_in(expiry_in_seconds):
        """
        Initializes a TTL object which will expire in expire_in_seconds seconds from when created.
        Remember to call .save() on the object after creation.
        :param expiry_in_seconds: How long should the TTL be in the DB, in seconds. Please take into consideration
        that the cleanup thread of mongo might take extra time to delete the TTL from the DB.
        """
        # Using UTC to make the mongodb TTL feature work. See
        # https://stackoverflow.com/questions/55994379/mongodb-ttl-index-doesnt-delete-expired-documents.
        return MonkeyTtl(expire_at=datetime.utcnow() + timedelta(seconds=expiry_in_seconds))

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


def create_monkey_ttl_document(expiry_duration_in_seconds):
    """
    Create a new Monkey TTL document and save it as a document.
    :param expiry_duration_in_seconds:  How long should the TTL last for. THIS IS A LOWER BOUND - depends on mongodb
    performance.
    :return: The TTL document. To get its ID use `.id`.
    """
    # The TTL data uses the new `models` module which depends on mongoengine.
    current_ttl = MonkeyTtl.create_ttl_expire_in(expiry_duration_in_seconds)
    current_ttl.save()
    return current_ttl
