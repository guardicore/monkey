from mongoengine import Document, FloatField


# TODO rename to Simulation, add other metadata
class AgentControls(Document):

    # Timestamp of the last "kill all agents" command
    last_stop_all = FloatField(default=None)
