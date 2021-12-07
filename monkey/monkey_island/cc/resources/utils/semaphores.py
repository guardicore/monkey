from gevent.lock import BoundedSemaphore

# Semaphore avoids race condition between monkeys
# being marked dead and monkey waking up as alive
AGENT_KILLING_SEMAPHORE = BoundedSemaphore()
