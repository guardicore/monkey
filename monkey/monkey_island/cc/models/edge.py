from mongoengine import (BooleanField, Document, DynamicField, ListField,
                         ObjectIdField, StringField)


class Edge(Document):

    meta = {'allow_inheritance': True}

    # SCHEMA
    src_node_id = ObjectIdField(required=True)
    dst_node_id = ObjectIdField(required=True)
    scans = ListField(DynamicField(), default=[])
    exploits = ListField(DynamicField(), default=[])
    tunnel = BooleanField(default=False)
    exploited = BooleanField(default=False)
    src_label = StringField()
    dst_label = StringField()
    group = StringField()
    domain_name = StringField()
    ip_address = StringField()
