from mongoengine import Document, FloatField


class AgentControls(Document):

    # Timestamp of the last "kill all agents" command
    last_stop_all = FloatField(default=None)
