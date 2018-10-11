from cc.services.pth_report_utils import PassTheHashReport, Machine
from cc.database import mongo
from bson import ObjectId


class PTHReportService(object):

    """

    """

    def __init__(self):
        pass


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
        # TODO: Fix bug if both local and non local account share the same password
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
    def old_get_shared_local_admins_nodes(pth):
        dups = dict(map(lambda x: (x, len(pth.GetSharedAdmins(x))), pth.machines))
        shared_admin_machines = []
        for m, count in sorted(dups.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if count <= 0:
                continue
            shared_admin_account_list = []

            for sid in pth.GetSharedAdmins(m):
                shared_admin_account_list.append(pth.GetUsernameBySid(sid))

            machine = {
                'ip': m.GetIp(),
                'hostname': m.GetHostName(),
                'domain': m.GetDomainName(),
                'services_names': m.GetCriticalServicesInstalled(),
                'user_count': count,
                'admins_accounts': shared_admin_account_list
            }

            shared_admin_machines.append(machine)

        return shared_admin_machines

    @staticmethod
    def get_strong_users_on_crit_services_by_machine(pth):
        threatening = dict(map(lambda x: (x, len(pth.GetThreateningUsersByVictim(x))), pth.GetCritialServers()))
        strong_users_crit_list = []

        for m, count in sorted(threatening.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if count <= 0:
                continue

            threatening_users_attackers_dict = {}
            for sid in pth.GetThreateningUsersByVictim(m):
                username = pth.GetUsernameBySid(sid)
                threatening_users_attackers_dict[username] = []
                for mm in pth.GetAttackersBySid(sid):
                    if m == mm:
                        continue
                    threatening_users_attackers_dict[username] = mm.GetIp()

            machine = {
                'ip': m.GetIp(),
                'hostname': m.GetHostName(),
                'domain': m.GetDomainName(),
                'services': m.GetCriticalServicesInstalled(),
                'threatening_users': threatening_users_attackers_dict
            }
            strong_users_crit_list.append(machine)
        return strong_users_crit_list

    @staticmethod
    def get_strong_users_on_crit_services_by_user(pth):
        critical_servers = pth.GetCritialServers()
        strong_users_dict = {}

        for server in critical_servers:
            users = pth.GetThreateningUsersByVictim(server)
            for sid in users:
                username = pth.GetUsernameBySid(sid)
                if username not in strong_users_dict:
                    strong_users_dict[username] = {
                        'services_names': [],
                        'machines': []
                    }
                strong_users_dict[username]['username'] = username
                strong_users_dict[username]['domain'] = server.GetDomainName()
                strong_users_dict[username]['services_names'] += server.GetCriticalServicesInstalled()
                strong_users_dict[username]['machines'].append(server.GetHostName())

        return strong_users_dict.values()

    @staticmethod
    def get_strong_users_on_non_crit_services(pth):
        threatening = dict(map(lambda x: (x, len(pth.GetThreateningUsersByVictim(x))), pth.GetNonCritialServers()))

        strong_users_non_crit_list = []

        for m, count in sorted(threatening.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if count <= 0:
                continue

            threatening_users_attackers_dict = {}
            for sid in pth.GetThreateningUsersByVictim(m):
                username = pth.GetUsernameBySid(sid)
                threatening_users_attackers_dict[username] = []
                for mm in pth.GetAttackersBySid(sid):
                    if m == mm:
                        continue
                    threatening_users_attackers_dict[username] = mm.GetIp()

            machine = {
                'ip': m.GetIp(),
                'hostname': m.GetHostName(),
                'domain': m.GetDomainName(),
                'services_names': [],
                'user_count': count,
                'threatening_users': threatening_users_attackers_dict
            }
            strong_users_non_crit_list.append(machine)
        return strong_users_non_crit_list




    @staticmethod
    def strong_users_on_crit_issues(strong_users):
        issues = []
        for machine in strong_users:
            issues.append(
                {
                    'type': 'strong_users_on_crit',
                    'machine': machine.get('hostname'),
                    'services': machine.get('services'),
                    'ip': machine.get('ip'),
                    'threatening_users': machine.get('threatening_users').keys()
                }
            )

        return issues

    @staticmethod
    def get_machine_details(node_id):
        machine = Machine(node_id)
        node = {}
        if machine.latest_system_info:
            node = {
                "id": str(node_id),
                "label": '{0} : {1}'.format(machine.GetHostName(), machine.GetIp()),
                'group': 'critical' if machine.IsCriticalServer() else 'normal',
                'users': list(machine.GetCachedUsernames()),
                'ips': [machine.GetIp()],
                'services': machine.GetCriticalServicesInstalled(),
                'hostname': machine.GetHostName()
            }
        return node

    @staticmethod
    def generate_map_nodes(pth):
        nodes_list = []
        for node_id in pth.vertices:
            node = PTHReportService.get_machine_details(node_id)
            nodes_list.append(node)

        return nodes_list

    @staticmethod
    def get_issues_list(issues):
        issues_dict = {}

        for issue in issues:
            machine = issue['machine']
            if machine not in issues_dict:
                issues_dict[machine] = []
            issues_dict[machine].append(issue)

        return issues_dict

    @staticmethod
    def get_report():



        issues = []
        pth = PassTheHashReport()

        strong_users_on_crit_services = PTHReportService.get_strong_users_on_crit_services_by_user(pth)
        strong_users_on_non_crit_services = PTHReportService.get_strong_users_on_non_crit_services(pth)

        issues += PTHReportService.get_duplicated_passwords_issues()
        # issues += PTHReportService.get_shared_local_admins_issues(local_admin_shared)
        # issues += PTHReportService.strong_users_on_crit_issues(
        #     PTHReportService.get_strong_users_on_crit_services_by_machine(pth))

        report = \
            {
                'report_info':
                    {
                        'strong_users_on_crit_services': strong_users_on_crit_services,
                        'strong_users_on_non_crit_services': strong_users_on_non_crit_services,
                        'pth_issues': issues
                    },
                'pthmap':
                    {
                        'nodes': PTHReportService.generate_map_nodes(pth),
                        'edges': pth.edges
                    }
            }
        return report