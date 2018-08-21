import json
import os
from shutil import copyfile

import sys
from flask import request, jsonify, make_response
import flask_restful

from cc.environment.environment import env
from cc.resources.monkey_download import get_monkey_executable
from cc.services.node import NodeService
from cc.utils import local_ip_addresses

__author__ = 'Barak'

import logging
logger = logging.getLogger(__name__)

def run_local_monkey():
    import platform
    import subprocess
    import stat

    # get the monkey executable suitable to run on the server
    result = get_monkey_executable(platform.system().lower(), platform.machine().lower())
    if not result:
        return False, "OS Type not found"

    monkey_path = os.path.join('binaries', result['filename'])
    target_path = os.path.join(os.getcwd(), result['filename'])

    # copy the executable to temp path (don't run the monkey from its current location as it may delete itself)
    try:
        copyfile(monkey_path, target_path)
        os.chmod(target_path, stat.S_IRWXU | stat.S_IRWXG)
    except Exception as exc:
        logger.error('Copy file failed', exc_info=True)
        return False, "Copy file failed: %s" % exc

    # run the monkey
    try:
        args = ['"%s" m0nk3y -s %s:%s' % (target_path, local_ip_addresses()[0], env.get_island_port())]
        if sys.platform == "win32":
            args = "".join(args)
        pid = subprocess.Popen(args, shell=True).pid
    except Exception as exc:
        logger.error('popen failed', exc_info=True)
        return False, "popen failed: %s" % exc

    return True, "pis: %s" % pid


class LocalRun(flask_restful.Resource):
    def get(self):
        NodeService.update_dead_monkeys()
        island_monkey = NodeService.get_monkey_island_monkey()
        if island_monkey is not None:
            is_monkey_running = not island_monkey["dead"]
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
