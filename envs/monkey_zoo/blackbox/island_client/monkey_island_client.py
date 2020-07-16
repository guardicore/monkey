import json
import logging
from time import sleep

from bson import json_util

from envs.monkey_zoo.blackbox.island_client.monkey_island_requests import \
    MonkeyIslandRequests

SLEEP_BETWEEN_REQUESTS_SECONDS = 0.5
MONKEY_TEST_ENDPOINT = 'api/test/monkey'
LOG_TEST_ENDPOINT = 'api/test/log'
LOGGER = logging.getLogger(__name__)


def avoid_race_condition(func):
    sleep(SLEEP_BETWEEN_REQUESTS_SECONDS)
    return func


class MonkeyIslandClient(object):
    def __init__(self, server_address):
        self.requests = MonkeyIslandRequests(server_address)

    def get_api_status(self):
        return self.requests.get("api")

    @avoid_race_condition
    def import_config(self, config_contents):
        _ = self.requests.post("api/configuration/island", data=config_contents)

    @avoid_race_condition
    def run_monkey_local(self):
        response = self.requests.post_json("api/local-monkey", data={"action": "run"})
        if MonkeyIslandClient.monkey_ran_successfully(response):
            LOGGER.info("Running the monkey.")
        else:
            LOGGER.error("Failed to run the monkey.")
            assert False

    @staticmethod
    def monkey_ran_successfully(response):
        return response.ok and json.loads(response.content)['is_running']

    @avoid_race_condition
    def kill_all_monkeys(self):
        if self.requests.get("api", {"action": "killall"}).ok:
            LOGGER.info("Killing all monkeys after the test.")
        else:
            LOGGER.error("Failed to kill all monkeys.")
            assert False

    @avoid_race_condition
    def reset_env(self):
        if self.requests.get("api", {"action": "reset"}).ok:
            LOGGER.info("Resetting environment after the test.")
        else:
            LOGGER.error("Failed to reset the environment.")
            assert False

    def find_monkeys_in_db(self, query):
        if query is None:
            raise TypeError
        response = self.requests.get(MONKEY_TEST_ENDPOINT,
                                     MonkeyIslandClient.form_find_query_for_request(query))
        return MonkeyIslandClient.get_test_query_results(response)

    def get_all_monkeys_from_db(self):
        response = self.requests.get(MONKEY_TEST_ENDPOINT,
                                     MonkeyIslandClient.form_find_query_for_request(None))
        return MonkeyIslandClient.get_test_query_results(response)

    def find_log_in_db(self, query):
        response = self.requests.get(LOG_TEST_ENDPOINT,
                                     MonkeyIslandClient.form_find_query_for_request(query))
        return MonkeyIslandClient.get_test_query_results(response)

    @staticmethod
    def form_find_query_for_request(query):
        return {'find_query': json_util.dumps(query)}

    @staticmethod
    def get_test_query_results(response):
        return json.loads(response.content)['results']

    def is_all_monkeys_dead(self):
        query = {'dead': False}
        return len(self.find_monkeys_in_db(query)) == 0

    def clear_caches(self):
        """
        Tries to clear caches.
        :raises: If error (by error code), raises the error
        :return: The response
        """
        response = self.requests.get("api/test/clear_caches")
        response.raise_for_status()
        return response
