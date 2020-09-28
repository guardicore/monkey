import json
import logging
import os
import sys
from shutil import copyfile

import flask_restful
from flask import jsonify, make_response, request

import monkey_island.cc.environment.environment_singleton as env_singleton
from monkey_island.cc.consts import MONKEY_ISLAND_ABS_PATH
from monkey_island.cc.models import Monkey
from monkey_island.cc.network_utils import local_ip_addresses
from monkey_island.cc.resources.monkey_download import get_monkey_executable
from monkey_island.cc.services.node import NodeService

__author__ = 'Barak'


logger = logging.getLogger(__name__)


def run_local_monkey():
    import platform
    import stat
    import subprocess

    # get the monkey executable suitable to run on the server
    result = get_monkey_executable(platform.system().lower(), platform.machine().lower())
    if not result:
        return False, "OS Type not found"

    monkey_path = os.path.join(MONKEY_ISLAND_ABS_PATH, 'cc', 'binaries', result['filename'])
    target_path = os.path.join(MONKEY_ISLAND_ABS_PATH, result['filename'])

    # copy the executable to temp path (don't run the monkey from its current location as it may delete itself)
    try:
        copyfile(monkey_path, target_path)
        os.chmod(target_path, stat.S_IRWXU | stat.S_IRWXG)
    except Exception as exc:
        logger.error('Copy file failed', exc_info=True)
        return False, "Copy file failed: %s" % exc

    # run the monkey
    try:
        args = ['"%s" m0nk3y -s %s:%s' % (target_path, local_ip_addresses()[0], env_singleton.env.get_island_port())]
        if sys.platform == "win32":
            args = "".join(args)
        pid = subprocess.Popen(args, shell=True).pid
    except Exception as exc:
        logger.error('popen failed', exc_info=True)
        return False, "popen failed: %s" % exc

    return True, ""


class LocalRun(flask_restful.Resource):
    def get(self):
        NodeService.update_dead_monkeys()
        island_monkey = NodeService.get_monkey_island_monkey()
        if island_monkey is not None:
            is_monkey_running = not Monkey.get_single_monkey_by_id(island_monkey["_id"]).is_dead()
        else:
            is_monkey_running = False

        return jsonify(is_running=is_monkey_running)

    def post(self):
        body = json.loads(request.data)
        if body.get('action') == 'run':
            local_run = run_local_monkey()
            return jsonify(is_running=local_run[0], error_text=local_run[1])

        # default action
        return make_response({'error': 'Invalid action'}, 500)
