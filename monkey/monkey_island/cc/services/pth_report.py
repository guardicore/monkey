from itertools import product

from cc.database import mongo
from bson import ObjectId

from cc.services.node import NodeService

__author__ = 'maor.rayzin'

class PTHReportService(object):

    @staticmethod
    def __dup_passwords_mongoquery():
        pipeline = [
            {"$match": {
                'NTLM_secret': {
                    "$exists": "true", "$ne": None}
            }},
            {
                "$group": {
                    "_id": {
                        "NTLM_secret": "$NTLM_secret"},
                    "count": {"$sum": 1},
                    "Docs": {"$push": {'_id': "$_id", 'name': '$name', 'domain_name': '$domain_name',
                                       'machine_id': '$machine_id'}}
                }},
            {'$match': {'count': {'$gt': 1}}}
        ]
        return mongo.db.groupsandusers.aggregate(pipeline)

    @staticmethod
    def __get_admin_on_machines_format(admin_on_machines):

        machines = mongo.db.monkey.find({'_id': {'$in': admin_on_machines}}, {'hostname': 1})
        return [i['hostname'] for i in list(machines)]

    @staticmethod
    def __strong_users_on_crit_query():
        pipeline = [
            {
                '$unwind': '$admin_on_machines'
            },
            {
                '$match': {'type': 1, 'domain_name': {'$ne': None}}
            },
            {
                '$lookup':
                    {
                        'from': 'monkey',
                        'localField': 'admin_on_machines',
                        'foreignField': '_id',
                        'as': 'critical_machine'
                    }
            },
            {
                '$match': {'critical_machine.critical_services': {'$ne': []}}
            },
            {
                '$unwind': '$critical_machine'
            }
        ]
        return mongo.db.groupsandusers.aggregate(pipeline)

    @staticmethod
    def get_duplicated_passwords_nodes():
        users_cred_groups = []
        docs = PTHReportService.__dup_passwords_mongoquery()
        for doc in docs:
            users_list = [
                {
                    'username': user['name'],
                    'domain_name': user['domain_name'],
                    'hostname': NodeService.get_hostname_by_id(ObjectId(user['machine_id'])) if user['machine_id'] else None
                 } for user in doc['Docs']
            ]
            users_cred_groups.append({'cred_groups': users_list})

        return users_cred_groups

    @staticmethod
    def get_duplicated_passwords_issues():
        user_groups = PTHReportService.get_duplicated_passwords_nodes()
        issues = []
        for group in user_groups:
            user_info = group['cred_groups'][0]
            issues.append(
                {
                    'type': 'shared_passwords_domain' if user_info['domain_name'] else 'shared_passwords',
                    'machine': user_info['hostname'] if user_info['hostname'] else user_info['domain_name'],
                    'shared_with': [i['username'] for i in group['cred_groups']],
                    'is_local': False if user_info['domain_name'] else True
                }
            )
        return issues

    @staticmethod
    def get_shared_admins_nodes():

        # This mongo queries users the best solution to figure out if an array
        # object has at least two objects in it, by making sure any value exists in the array index 1.
        admins = mongo.db.groupsandusers.find({'type': 1, 'admin_on_machines.1': {'$exists': True}},
                                              {'admin_on_machines': 1, 'name': 1, 'domain_name': 1})
        return [
            {
                'name': admin['name'],
                'domain_name': admin['domain_name'],
                'admin_on_machines': PTHReportService.__get_admin_on_machines_format(admin['admin_on_machines'])
            } for admin in admins
        ]

    @staticmethod
    def get_shared_admins_issues():
        admins_info = PTHReportService.get_shared_admins_nodes()
        return [
            {
                    'is_local': False,
                    'type': 'shared_admins_domain',
                    'machine': admin['domain_name'],
                    'username': admin['name'],
                    'shared_machines': admin['admin_on_machines'],
            }
            for admin in admins_info]

    @staticmethod
    def get_strong_users_on_critical_machines_nodes():

        crit_machines = {}
        docs = PTHReportService.__strong_users_on_crit_query()

        for doc in docs:
            hostname = str(doc['critical_machine']['hostname'])
            if hostname not in crit_machines:
                crit_machines[hostname] = {
                    'threatening_users': [],
                    'critical_services': doc['critical_machine']['critical_services']
                }
            crit_machines[hostname]['threatening_users'].append(
                {'name': str(doc['domain_name']) + '\\' + str(doc['name']),
                 'creds_location': doc['secret_location']})
        return crit_machines

    @staticmethod
    def get_strong_users_on_crit_issues():
        crit_machines = PTHReportService.get_strong_users_on_critical_machines_nodes()

        return [
            {
                'type': 'strong_users_on_crit',
                'machine': machine,
                'services': crit_machines[machine].get('critical_services'),
                'threatening_users': [i['name'] for i in crit_machines[machine]['threatening_users']]
            } for machine in crit_machines
        ]

    @staticmethod
    def get_strong_users_on_crit_details():
        user_details = {}
        crit_machines = PTHReportService.get_strong_users_on_critical_machines_nodes()
        for machine in crit_machines:
            for user in crit_machines[machine]['threatening_users']:
                username = user['name']
                if username not in user_details:
                    user_details[username] = {
                        'machines': [],
                        'services': []
                    }
                user_details[username]['machines'].append(machine)
                user_details[username]['services'] += crit_machines[machine]['critical_services']

        return [
            {
                'username': user,
                'machines': user_details[user]['machines'],
                'services_names': user_details[user]['services']
            } for user in user_details
        ]

    @staticmethod
    def generate_map_nodes():
        monkeys = mongo.db.monkey.find({}, {'_id': 1, 'hostname': 1, 'critical_services': 1, 'ip_addresses': 1})

        return [
            {
                'id': monkey['_id'],
                'label': '{0} : {1}'.format(monkey['hostname'], monkey['ip_addresses'][0]),
                'group': 'critical' if monkey.get('critical_services', []) else 'normal',
                'services': monkey.get('critical_services', []),
                'hostname': monkey['hostname']
            } for monkey in monkeys
        ]

    @staticmethod
    def generate_edges():
        edges_list = []

        comp_users = mongo.db.groupsandusers.find(
            {
                'admin_on_machines': {'$ne': []},
                'secret_location': {'$ne': []},
                'type': 1
            },
            {
                'admin_on_machines': 1, 'secret_location': 1
            }
        )

        for user in comp_users:
            # A list comp, to get all unique pairs of attackers and victims.
            for pair in [pair for pair in product(user['admin_on_machines'], user['secret_location'])
                         if pair[0] != pair[1]]:
                edges_list.append(
                    {
                        'from': pair[1],
                        'to': pair[0],
                        'id': str(pair[1]) + str(pair[0])
                    }
                )
        return edges_list

    @staticmethod
    def get_pth_map():
        return {
            'nodes': PTHReportService.generate_map_nodes(),
            'edges': PTHReportService.generate_edges()
            }

    @staticmethod
    def get_report():
        pth_map = PTHReportService.get_pth_map()
        PTHReportService.get_strong_users_on_critical_machines_nodes()
        report = \
            {
                'report_info':
                    {
                        'strong_users_table': PTHReportService.get_strong_users_on_crit_details()
                    },

                'pthmap':
                    {
                        'nodes': pth_map.get('nodes'),
                        'edges': pth_map.get('edges')
                    }
            }

        return report

