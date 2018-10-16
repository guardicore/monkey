import uuid
from itertools import combinations, product

from cc.database import mongo
from bson import ObjectId


class PTHReportService(object):

    @staticmethod
    def get_duplicated_passwords_nodes():
        users_cred_groups = []

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
        docs = mongo.db.groupsandusers.aggregate(pipeline)
        for doc in docs:
            users_list = []
            for user in doc['Docs']:
                hostname = None
                if user['machine_id']:
                    machine = mongo.db.monkey.find_one({'_id': ObjectId(user['machine_id'])}, {'hostname': 1})
                    if machine.get('hostname'):
                        hostname = machine['hostname']
                users_list.append({'username': user['name'], 'domain_name': user['domain_name'],
                                   'hostname': hostname})
            users_cred_groups.append({'cred_groups': users_list})

        return users_cred_groups

    @staticmethod
    def get_duplicated_passwords_issues():
        user_groups = PTHReportService.get_duplicated_passwords_nodes()
        issues = []
        users_gathered = []
        for group in user_groups:
            for user_info in group['cred_groups']:
                users_gathered.append(user_info['username'])
                issues.append(
                    {
                        'type': 'shared_passwords_domain' if user_info['domain_name'] else 'shared_passwords',
                        'machine': user_info['hostname'] if user_info['hostname'] else user_info['domain_name'],
                        'shared_with': [i['username'] for i in group['cred_groups']],
                        'is_local': False if user_info['domain_name'] else True
                    }
                )
                break
        return issues

    @staticmethod
    def get_shared_admins_nodes():
        admins = mongo.db.groupsandusers.find({'type': 1, 'admin_on_machines.1': {'$exists': True}},
                                              {'admin_on_machines': 1, 'name': 1, 'domain_name': 1})
        admins_info_list = []
        for admin in admins:
            machines = mongo.db.monkey.find({'_id': {'$in': admin['admin_on_machines']}}, {'hostname': 1})

            # appends the host names of the machines this user is admin on.
            admins_info_list.append({'name': admin['name'],'domain_name': admin['domain_name'],
                                     'admin_on_machines': [i['hostname'] for i in list(machines)]})

        return admins_info_list

    @staticmethod
    def get_shared_admins_issues():
        admins_info = PTHReportService.get_shared_admins_nodes()
        issues = []
        for admin in admins_info:
            issues.append(
                {
                    'is_local': False,
                    'type': 'shared_admins_domain',
                    'machine': admin['domain_name'],
                    'username': admin['name'],
                    'shared_machines': admin['admin_on_machines'],
                }
            )

        return issues

    @staticmethod
    def get_strong_users_on_critical_machines_nodes():
        crit_machines = {}
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
        docs = mongo.db.groupsandusers.aggregate(pipeline)
        for doc in docs:
            hostname = str(doc['critical_machine']['hostname'])
            if not hostname in crit_machines:
                crit_machines[hostname] = {}
                crit_machines[hostname]['threatening_users'] = []
                crit_machines[hostname]['critical_services'] = doc['critical_machine']['critical_services']
            crit_machines[hostname]['threatening_users'].append(
                {'name': str(doc['domain_name']) + '\\' + str(doc['name']),
                 'creds_location': doc['secret_location']})
        return crit_machines

    @staticmethod
    def get_strong_users_on_crit_issues():
        issues = []
        crit_machines = PTHReportService.get_strong_users_on_critical_machines_nodes()
        for machine in crit_machines:
            issues.append(
                {
                    'type': 'strong_users_on_crit',
                    'machine': machine,
                    'services': crit_machines[machine].get('critical_services'),
                    'threatening_users': [i['name'] for i in crit_machines[machine]['threatening_users']]
                }
            )

        return issues

    @staticmethod
    def get_strong_users_on_crit_details():
        table_entries = []
        user_details = {}
        crit_machines = PTHReportService.get_strong_users_on_critical_machines_nodes()
        for machine in crit_machines:
            for user in crit_machines[machine]['threatening_users']:
                username = user['name']
                if username not in user_details:
                    user_details[username] = {}
                    user_details[username]['machines'] = []
                    user_details[username]['services'] = []
                user_details[username]['machines'].append(machine)
                user_details[username]['services'] += crit_machines[machine]['critical_services']

        for user in user_details:
            table_entries.append(
                {
                    'username': user,
                    'machines': user_details[user]['machines'],
                    'services_names': user_details[user]['services']
                }
            )

        return table_entries

    @staticmethod
    def generate_map_nodes():

        nodes_list = []
        monkeys = mongo.db.monkey.find({}, {'_id': 1, 'hostname': 1, 'critical_services': 1, 'ip_addresses': 1})
        for monkey in monkeys:
            critical_services = monkey.get('critical_services', [])
            nodes_list.append({
                'id': monkey['_id'],
                'label': '{0} : {1}'.format(monkey['hostname'], monkey['ip_addresses'][0]),
                'group': 'critical' if critical_services else 'normal',
                'services': critical_services,
                'hostname': monkey['hostname']
            })

        return nodes_list

    @staticmethod
    def generate_edge_nodes():
        edges_list = []
        pipeline = [
            {
                '$match': {'admin_on_machines': {'$ne': []}, 'secret_location': {'$ne': []}, 'type': 1}
            },
            {
                '$project': {'admin_on_machines': 1, 'secret_location': 1}
            }
        ]
        comp_users = mongo.db.groupsandusers.aggregate(pipeline)

        for user in comp_users:
            pairs = PTHReportService.generate_edges_tuples(user['admin_on_machines'], user['secret_location'])
            for pair in pairs:
                edges_list.append(
                    {
                        'from': pair[1],
                        'to': pair[0],
                        'id': str(uuid.uuid4())
                    }
                )
        return edges_list

    @staticmethod
    def generate_edges_tuples(*lists):

        for t in combinations(lists, 2):
            for pair in product(*t):
                # Don't output pairs containing duplicated elements
                if pair[0] != pair[1]:
                    yield pair

    @staticmethod
    def get_pth_map():
        return {
            'nodes': PTHReportService.generate_map_nodes(),
            'edges': PTHReportService.generate_edge_nodes()
            }

    @staticmethod
    def get_report():

        PTHReportService.get_strong_users_on_critical_machines_nodes()
        report = \
            {
                'report_info':
                    {
                        'strong_users_table': PTHReportService.get_strong_users_on_crit_details()
                    },

                'pthmap':
                    {
                        'nodes': PTHReportService.generate_map_nodes(),
                        'edges': PTHReportService.generate_edge_nodes()
                    }
            }

        return report

