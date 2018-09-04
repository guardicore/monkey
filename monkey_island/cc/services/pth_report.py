from cc.services.pth_report_utils import PassTheHashReport, Machine


class PTHReportService(object):

    """

    """

    def __init__(self):
        pass

    @staticmethod
    def get_duplicated_password_nodes(pth):
        """

        """

        usernames_lists = []
        usernames_per_sid_list = []
        dups = dict(map(lambda x: (x, len(pth.GetSidsBySecret(x))), pth.GetAllSecrets()))

        for secret, count in sorted(dups.iteritems(), key=lambda (k, v): (v, k), reverse=True):
            if count <= 1:
                continue
            for sid in pth.GetSidsBySecret(secret):
                if sid:
                    usernames_per_sid_list.append(pth.GetUsernameBySid(sid))

            usernames_lists.append({'cred_group': usernames_per_sid_list})

        return usernames_lists

    @staticmethod
    def get_shared_local_admins_nodes(pth):
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
    def get_duplicated_passwords_issues(pth, password_groups):
        issues = []
        previeous_group = []
        for group in password_groups:
            username = group['cred_group'][0]
            if username in previeous_group:
                continue
            sid = list(pth.GetSidsByUsername(username.split('\\')[1]))
            machine_info = pth.GetSidInfo(sid[0])
            issues.append(
                {
                    'type': 'shared_passwords',
                    'machine': machine_info.get('hostname').split('.')[0],
                    'shared_with': group['cred_group']
                }
            )
            previeous_group += group['cred_group']

        return issues

    @staticmethod
    def get_shared_local_admins_issues(shared_admins_machines):
        issues = []
        for machine in shared_admins_machines:
            issues.append(
                {
                    'type': 'shared_admins',
                    'machine': machine.get('hostname'),
                    'shared_accounts': machine.get('admins_accounts'),
                    'ip': machine.get('ip'),
                }
            )

        return issues

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

        same_password = PTHReportService.get_duplicated_password_nodes(pth)
        local_admin_shared = PTHReportService.get_shared_local_admins_nodes(pth)
        strong_users_on_crit_services = PTHReportService.get_strong_users_on_crit_services_by_user(pth)
        strong_users_on_non_crit_services = PTHReportService.get_strong_users_on_non_crit_services(pth)

        issues += PTHReportService.get_duplicated_passwords_issues(pth, same_password)
        issues += PTHReportService.get_shared_local_admins_issues(local_admin_shared)
        issues += PTHReportService.strong_users_on_crit_issues(
            PTHReportService.get_strong_users_on_crit_services_by_machine(pth))

        report = \
            {
                'report_info':
                    {
                        'same_password': same_password,
                        'local_admin_shared': local_admin_shared,
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