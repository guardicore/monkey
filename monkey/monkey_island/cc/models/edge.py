from mongoengine import Document, ObjectIdField, ListField, DynamicField, BooleanField, StringField


class Edge(Document):
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
