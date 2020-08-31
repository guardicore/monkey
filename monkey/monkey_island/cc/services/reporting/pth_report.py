from itertools import product

from bson import ObjectId

from monkey_island.cc.database import mongo
from monkey_island.cc.models import Monkey
from monkey_island.cc.services.groups_and_users_consts import USERTYPE
from monkey_island.cc.services.node import NodeService

__author__ = 'maor.rayzin'


class PTHReportService(object):
    """
    A static class supplying utils to produce a report based on the PTH related information
    gathered via mimikatz and wmi.
    """

    @staticmethod
    def __dup_passwords_mongoquery():
        """
            This function builds and queries the mongoDB for users that are using the same passwords. this is done
            by comparing the NTLM hash found for each user by mimikatz.
        :return:
            A list of mongo documents (dicts in python) that look like this:
            {
                '_id': The NTLM hash,
                'count': How many users share it.
                'Docs': the name, domain name, _Id, and machine_id of the users
            }
        """

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
    def __get_admin_on_machines_format(admin_on_machines, domain_name):
        """
        This function finds for each admin user, which machines its an admin of, and compile them to a list.
        :param admin_on_machines: A list of "monkey" documents "_id"s
        :param domain_name: The admins' domain name
        :return:
        A list of formatted machines names *domain*/*hostname*, to use in shared admins issues.
        """
        machines = mongo.db.monkey.find({'_id': {'$in': admin_on_machines}}, {'hostname': 1})
        return [domain_name + '\\' + i['hostname'] for i in list(machines)]

    @staticmethod
    def __strong_users_on_crit_query():
        """
            This function build and query the mongoDB for users that mimikatz was able to find cached NTLM hashes and
            are administrators on machines with services predefined as important services thus making these machines
            critical.
        :return:
            A list of said users
        """
        pipeline = [
            {
                '$unwind': '$admin_on_machines'
            },
            {
                '$match': {'type': USERTYPE, 'domain_name': {'$ne': None}}
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
    def __build_dup_user_label(i):
        return i['hostname'] + '\\' + i['username'] if i['hostname'] else i['domain_name'] + '\\' + i['username']

    @staticmethod
    def get_duplicated_passwords_nodes():
        users_cred_groups = []
        docs = PTHReportService.__dup_passwords_mongoquery()
        for doc in docs:
            users_list = [
                {
                    'username': user['name'],
                    'domain_name': user['domain_name'],
                    'hostname': NodeService.get_hostname_by_id(ObjectId(user['machine_id'])) if
                    user['machine_id'] else None
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
                    'shared_with': [PTHReportService.__build_dup_user_label(i) for i in group['cred_groups']],
                    'is_local': False if user_info['domain_name'] else True
                }
            )
        return issues

    @staticmethod
    def get_shared_admins_nodes():

        # This mongo queries users the best solution to figure out if an array
        # object has at least two objects in it, by making sure any value exists in the array index 1.
        # Excluding the name Administrator - its spamming the lists and not a surprise the domain Administrator account
        # is shared.
        admins = mongo.db.groupsandusers.find({'type': USERTYPE, 'name': {'$ne': 'Administrator'},
                                               'admin_on_machines.1': {'$exists': True}},
                                              {'admin_on_machines': 1, 'name': 1, 'domain_name': 1})
        return [
            {
                'name': admin['name'],
                'domain_name': admin['domain_name'],
                'admin_on_machines': PTHReportService.__get_admin_on_machines_format(admin['admin_on_machines'],
                                                                                     admin['domain_name'])
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
                'username': admin['domain_name'] + '\\' + admin['name'],
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
        monkeys = [m for m in Monkey.objects() if m.get_os() == "windows"]

        return [
            {
                'id': monkey.guid,
                'label': '{0} : {1}'.format(monkey.hostname, monkey.ip_addresses[0]),
                'group': 'critical' if monkey.critical_services is not None else 'normal',
                'services': monkey.critical_services,
                'hostname': monkey.hostname
            } for monkey in monkeys
        ]

    @staticmethod
    def generate_edges():
        edges_list = []

        comp_users = mongo.db.groupsandusers.find(
            {
                'admin_on_machines': {'$ne': []},
                'secret_location': {'$ne': []},
                'type': USERTYPE
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
