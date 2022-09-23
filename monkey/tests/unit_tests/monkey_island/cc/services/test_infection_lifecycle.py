import uuid

from monkey_island.cc.models import Config, Monkey


def create_monkey(launch_time):
    monkey = Monkey(guid=str(uuid.uuid4()))
    monkey.config = Config()
    monkey.should_stop = False
    monkey.launch_time = launch_time
    monkey.save()
    return monkey


def create_parent(child_monkey, launch_time):
    monkey_parent = Monkey(guid=str(uuid.uuid4()))
    child_monkey.parent = [[monkey_parent.guid]]
    monkey_parent.launch_time = launch_time
    monkey_parent.save()
    child_monkey.save()
