import json

import os
from flask import request, send_from_directory
import flask_restful

__author__ = 'Barak'


MONKEY_DOWNLOADS = [
    {
        'type': 'linux',
        'machine': 'x86_64',
        'filename': 'monkey-linux-64',
    },
    {
        'type': 'linux',
        'machine': 'i686',
        'filename': 'monkey-linux-32',
    },
    {
        'type': 'linux',
        'filename': 'monkey-linux-64',
    },
    {
        'type': 'windows',
        'machine': 'x86',
        'filename': 'monkey-windows-32.exe',
    },
    {
        'type': 'windows',
        'machine': 'amd64',
        'filename': 'monkey-windows-64.exe',
    },
    {
        'type': 'windows',
        'filename': 'monkey-windows-32.exe',
    },
]


def get_monkey_executable(host_os, machine):
    for download in MONKEY_DOWNLOADS:
        if host_os == download.get('type') and machine == download.get('machine'):
            return download
    return None


class MonkeyDownload(flask_restful.Resource):
    def get(self, path):
        return send_from_directory('binaries', path)

    def post(self):
        host_json = json.loads(request.data)
        host_os = host_json.get('os')
        if host_os:
            result = get_monkey_executable(host_os.get('type'), host_os.get('machine'))

            if result:
                real_path = os.path.join('binaries', result['filename'])
                if os.path.isfile(real_path):
                    result['size'] = os.path.getsize(real_path)
                    return result

        return {}
