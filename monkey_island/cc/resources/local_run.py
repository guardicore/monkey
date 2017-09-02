import json
import os
from shutil import copyfile

import sys
from flask import request, jsonify, make_response
import flask_restful

from cc.resources.monkey_download import get_monkey_executable

from cc.utils import local_ips

__author__ = 'Barak'


def run_local_monkey(island_address):
    import platform
    import subprocess
    import stat

    # get the monkey executable suitable to run on the server
    result = get_monkey_executable(platform.system().lower(), platform.machine().lower())
    if not result:
        return (False, "OS Type not found")

    monkey_path = os.path.join('binaries', result['filename'])
    target_path = os.path.join(os.getcwd(), result['filename'])

    # copy the executable to temp path (don't run the monkey from its current location as it may delete itself)
    try:
        copyfile(monkey_path, target_path)
        os.chmod(target_path, stat.S_IRWXU | stat.S_IRWXG)
    except Exception, exc:
        return (False, "Copy file failed: %s" % exc)

    # run the monkey
    try:
        args = ["%s m0nk3y -s %s:%s" % (target_path, island_address, ISLAND_PORT)]
        if sys.platform == "win32":
            args = "".join(args)
        pid = subprocess.Popen(args, shell=True).pid
    except Exception, exc:
        return (False, "popen failed: %s" % exc)

    return (True, "pis: %s" % pid)


class LocalRun(flask_restful.Resource):
    def get(self):
        # TODO implement is_running from db monkeys collection
        return jsonify(is_running=False)

    def post(self):
        body = json.loads(request.data)
        if body.get('action') == 'run' and body.get('ip') is not None:
            local_run = run_local_monkey(island_address=body.get('ip'))
            return jsonify(is_running=local_run[0])

        # default action
        return make_response({'error': 'Invalid action'}, 500)
