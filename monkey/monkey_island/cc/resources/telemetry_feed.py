from datetime import datetime

import dateutil
import flask_restful
from flask import request
import flask_pymongo

from monkey_island.cc.auth import jwt_required
from monkey_island.cc.database import mongo
from monkey_island.cc.services.node import NodeService

__author__ = 'itay.mizeretz'


class TelemetryFeed(flask_restful.Resource):
    @jwt_required()
    def get(self, **kw):
        timestamp = request.args.get('timestamp')
        if "null" == timestamp or timestamp is None:  # special case to avoid ugly JS code...
            telemetries = mongo.db.telemetry.find({})
        else:
            telemetries = mongo.db.telemetry.find({'timestamp': {'$gt': dateutil.parser.parse(timestamp)}})\

        telemetries = telemetries.sort([('timestamp', flask_pymongo.ASCENDING)])

        return \
            {
                'telemetries': [TelemetryFeed.get_displayed_telemetry(telem) for telem in telemetries],
                'timestamp': datetime.now().isoformat()
            }

    @staticmethod
    def get_displayed_telemetry(telem):
        monkey = NodeService.get_monkey_by_guid(telem['monkey_guid'])
        default_hostname = "GUID-" + telem['monkey_guid']
        return \
            {
                'id': telem['_id'],
                'timestamp': telem['timestamp'].strftime('%d/%m/%Y %H:%M:%S'),
                'hostname': monkey.get('hostname', default_hostname) if monkey else default_hostname,
                'brief': TELEM_PROCESS_DICT[telem['telem_catagory']](telem)
            }

    @staticmethod
    def get_tunnel_telem_brief(telem):
        tunnel = telem['data']['proxy']
        if tunnel is None:
            return 'No tunnel is used.'
        else:
            tunnel_host_ip = tunnel.split(":")[-2].replace("//", "")
            tunnel_host = NodeService.get_monkey_by_ip(tunnel_host_ip)['hostname']
            return 'Tunnel set up to machine: %s.' % tunnel_host

    @staticmethod
    def get_state_telem_brief(telem):
        if telem['data']['done']:
            return '''Monkey finishing its execution.'''
        else:
            return 'Monkey started.'

    @staticmethod
    def get_exploit_telem_brief(telem):
        target = telem['data']['machine']['ip_addr']
        exploiter = telem['data']['exploiter']
        result = telem['data']['result']
        if result:
            return 'Monkey successfully exploited %s using the %s exploiter.' % (target, exploiter)
        else:
            return 'Monkey failed exploiting %s using the %s exploiter.' % (target, exploiter)

    @staticmethod
    def get_scan_telem_brief(telem):
        return 'Monkey discovered machine %s.' % telem['data']['machine']['ip_addr']

    @staticmethod
    def get_systeminfo_telem_brief(telem):
        return 'Monkey collected system information.'

    @staticmethod
    def get_trace_telem_brief(telem):
        return 'Monkey reached max depth.'

    @staticmethod
    def get_post_breach_telem_brief(telem):
        return '%s post breach action executed on %s (%s) machine' % (telem['data']['name'],
                                                                      telem['data']['hostname'],
                                                                      telem['data']['ip'])

    @staticmethod
    def get_attack_telem_brief(telem):
        return 'Monkey collected MITRE ATT&CK info.'


TELEM_PROCESS_DICT = \
    {
        'tunnel': TelemetryFeed.get_tunnel_telem_brief,
        'state': TelemetryFeed.get_state_telem_brief,
        'exploit': TelemetryFeed.get_exploit_telem_brief,
        'scan': TelemetryFeed.get_scan_telem_brief,
        'system_info_collection': TelemetryFeed.get_systeminfo_telem_brief,
        'trace': TelemetryFeed.get_trace_telem_brief,
        'post_breach': TelemetryFeed.get_post_breach_telem_brief,
        'attack': TelemetryFeed.get_attack_telem_brief
    }
