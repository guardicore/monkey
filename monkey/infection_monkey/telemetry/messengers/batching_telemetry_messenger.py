import queue
import threading
import time
from typing import Dict

from infection_monkey.telemetry.i_batchable_telem import IBatchableTelem
from infection_monkey.telemetry.i_telem import ITelem
from infection_monkey.telemetry.messengers.i_telemetry_messenger import ITelemetryMessenger

DEFAULT_PERIOD = 5
WAKES_PER_PERIOD = 4


class BatchingTelemetryMessenger(ITelemetryMessenger):
    """
    An ITelemetryMessenger decorator that aggregates IBatchableTelem telemetries
    and periodically sends them to Monkey Island.
    """

    def __init__(self, telemetry_messenger: ITelemetryMessenger, period=DEFAULT_PERIOD):
        self._queue: queue.Queue[ITelem] = queue.Queue()
        self._thread = BatchingTelemetryMessenger._BatchingTelemetryMessengerThread(
            self._queue, telemetry_messenger, period
        )

        self._thread.start()

    def __del__(self):
        self._thread.stop()

    def send_telemetry(self, telemetry: ITelem):
        self._queue.put(telemetry)

    class _BatchingTelemetryMessengerThread:
        def __init__(self, queue: queue.Queue, telemetry_messenger: ITelemetryMessenger, period):
            self._queue: queue.Queue[ITelem] = queue
            self._telemetry_messenger = telemetry_messenger
            self._period = period

            self._should_run_batch_thread = True
            # TODO: Create a "timer" or "countdown" class and inject an object instead of
            #       using time.time()
            self._last_sent_time = time.time()
            self._telemetry_batches: Dict[str, IBatchableTelem] = {}

        def start(self):
            self._should_run_batch_thread = True
            self._manage_telemetry_batches_thread = threading.Thread(
                target=self._manage_telemetry_batches
            )
            self._manage_telemetry_batches_thread.start()

        def stop(self):
            self._should_run_batch_thread = False
            self._manage_telemetry_batches_thread.join()

        def _manage_telemetry_batches(self):
            self._reset()

            while self._should_run_batch_thread or not self._queue.empty():
                try:
                    telemetry = self._queue.get(block=True, timeout=self._period / WAKES_PER_PERIOD)

                    if isinstance(telemetry, IBatchableTelem):
                        self._add_telemetry_to_batch(telemetry)
                    else:
                        self._telemetry_messenger.send_telemetry(telemetry)
                except queue.Empty:
                    pass

                if self._period_elapsed():
                    self._send_telemetry_batches()
                    self._reset()

            self._send_telemetry_batches()

        def _reset(self):
            self._last_sent_time = time.time()
            self._telemetry_batches = {}

        def _add_telemetry_to_batch(self, new_telemetry: IBatchableTelem):
            telem_category = new_telemetry.telem_category

            if telem_category in self._telemetry_batches:
                self._telemetry_batches[telem_category].add_telemetry_to_batch(new_telemetry)
            else:
                self._telemetry_batches[telem_category] = new_telemetry

        def _period_elapsed(self):
            return (time.time() - self._last_sent_time) > self._period

        def _send_telemetry_batches(self):
            for batchable_telemetry in self._telemetry_batches.values():
                self._telemetry_messenger.send_telemetry(batchable_telemetry)
