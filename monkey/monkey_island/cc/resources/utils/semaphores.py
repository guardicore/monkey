# TODO: Switch to threading.lock and test. Calling gevent.patch_all() is supposed to monkeypatch
#       threading to be compatible with gevent/greenlets.
from gevent.lock import BoundedSemaphore

# Mutex avoids race condition between monkeys
# being marked dead and monkey waking up as alive
agent_killing_mutex = BoundedSemaphore()
