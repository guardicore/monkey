from monkey_island.cc.environment import Environment


# TODO: We can probably remove these Environment subclasses, but the
#       AwsEnvironment class still does something unique in its constructor.
class PasswordEnvironment(Environment):
    pass
