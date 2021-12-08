from gevent.lock import BoundedSemaphore

# Mutex avoids race condition between monkeys
# being marked dead and monkey waking up as alive
agent_killing_mutex = BoundedSemaphore()
