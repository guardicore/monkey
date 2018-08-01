import hashlib
import binascii
import copy
import uuid

from cc.database import mongo
from cc.services.node import NodeService

DsRole_RoleStandaloneWorkstation = 0
DsRole_RoleMemberWorkstation = 1
DsRole_RoleStandaloneServer = 2
DsRole_RoleMemberServer = 3
DsRole_RoleBackupDomainController = 4
DsRole_RolePrimaryDomainController = 5

SidTypeUser = 1
SidTypeGroup = 2
SidTypeDomain = 3
SidTypeAlias = 4
SidTypeWellKnownGroup = 5
SidTypeDeletedAccount = 6
SidTypeInvalid = 7
SidTypeUnknown = 8
SidTypeComputer = 9



def is_group_sid_type(type):
    return type in (SidTypeGroup, SidTypeAlias, SidTypeWellKnownGroup)


def myntlm(x):
    hash = hashlib.new('md4', x.encode('utf-16le')).digest()
    return str(binascii.hexlify(hash))


def cache(foo):
    def hash(o):
        if type(o) in (int, float, str, unicode):
            return repr(o)

        elif type(o) in (type(None),):
            return "___None___"

        elif type(o) in (list, tuple, set):
            hashed = tuple([hash(x) for x in o])

            if "NotHashable" in hashed:
                return "NotHashable"

            return hashed

        elif type(o) == dict:
            hashed_keys = tuple([hash(k) for k, v in o.iteritems()])
            hashed_vals = tuple([hash(v) for k, v in o.iteritems()])

            if "NotHashable" in hashed_keys or "NotHashable" in hashed_vals:
                return "NotHashable"

            return tuple(zip(hashed_keys, hashed_vals))

        elif type(o) == Machine:
            return o.monkey_guid

        #        elif type(o) == PthMap:
        #            return "PthMapSingleton"

        elif type(o) == PassTheHashReport:
            return "PassTheHashReportSingleton"

        else:
            assert False, "%s of type %s is not hashable" % (repr(o), type(o))
            return "NotHashable"

    def wrapper(*args, **kwargs):
        hashed = (hash(args), hash(kwargs))

        if "NotHashable" in hashed:
            return foo(*args, **kwargs)

        if not hasattr(foo, "_mycache_"):
            foo._mycache_ = dict()

        if hashed not in foo._mycache_.keys():
            foo._mycache_[hashed] = foo(*args, **kwargs)

        return copy.deepcopy(foo._mycache_[hashed])

    return wrapper


class Machine(object):
    def __init__(self, monkey_guid):
        self.monkey_guid = str(monkey_guid)

        self.latest_system_info = mongo.db.telemetry.find(
            {"telem_type": "system_info_collection", "monkey_guid": self.monkey_guid}).sort([("timestamp", -1)]).limit(
            1)

        if self.latest_system_info.count() > 0:
            self.latest_system_info = self.latest_system_info[0]

        self.monkey_info = NodeService.get_monkey_by_guid(self.monkey_guid)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.monkey_guid == other.monkey_guid
        else:
            return False

    @cache
    def GetMimikatzOutput(self):
        doc = self.latest_system_info

        if not doc:
            return None

        return doc.get("data").get("mimikatz")

    @cache
    def GetHostName(self):
        doc = self.latest_system_info

        for comp in doc.get("data").get("Win32_ComputerSystem", {}):
            return eval(comp.get("Name"))

        return None

    @cache
    def GetIp(self):
        doc = self.latest_system_info

        for addr in doc.get("data").get("network_info", {}).get("networks", {}):
            return str(addr["addr"])

        return None

    @cache
    def get_monkey_id(self):
        doc = self.monkey_info

        return str(doc.get('_id'))

    @cache
    def GetDomainName(self):
        doc = self.latest_system_info

        for comp in doc.get("data").get("Win32_ComputerSystem", {}):
            return eval(comp.get("Domain"))

        return None

    @cache
    def GetDomainRole(self):
        doc = self.latest_system_info

        for comp in doc.get("data").get("Win32_ComputerSystem", {}):
            return comp.get("DomainRole")

        return None

    @cache
    def IsDomainController(self):
        return self.GetDomainRole() in (DsRole_RolePrimaryDomainController, DsRole_RoleBackupDomainController)

    @cache
    def GetSidByUsername(self, username, domain=None):
        doc = self.latest_system_info

        for user in doc.get("data").get("Win32_UserAccount", {}):
            if eval(user.get("Name")) != username:
                continue

            if user.get("SIDType") != SidTypeUser:
                continue

            if domain and user.get("Domain") != domain:
                continue

            return eval(user.get("SID"))

        if not self.IsDomainController():
            for dc in self.GetDomainControllers():
                sid = dc.GetSidByUsername(username)

                if sid != None:
                    return sid

        return None

    @cache
    def GetUsernameBySid(self, sid):
        info = self.GetSidInfo(sid)

        if not info:
            return None

        return str(info.get("Domain")) + "\\" + str(info.get("Username"))

    @cache
    def GetSidInfo(self, sid):
        doc = self.latest_system_info

        for user in doc.get("data").get("Win32_UserAccount",{}):
            if eval(user.get("SID")) != sid:
                continue

            if user.get("SIDType") != SidTypeUser:
                continue

            return {"Domain": eval(user.get("Domain")),
                    "Username": eval(user.get("Name")),
                    "Disabled": user.get("Disabled") == "true",
                    "PasswordRequired": user.get("PasswordRequired") == "true",
                    "PasswordExpires": user.get("PasswordExpires") == "true",
                    'hostname': doc.get('data').get('hostname'), }

        if not self.IsDomainController():
            for dc in self.GetDomainControllers():
                domain = dc.GetSidInfo(sid)

                if domain != None:
                    return domain

        return None

    @cache
    def GetCriticalServicesInstalled(self):
        def IsNameOfCriticalService(name):
            services = ("W3svc", "MSExchangeServiceHost", "MSSQLServer", "dns")
            services = map(str.lower, services)

            if not name:
                return False

            name = name.lower()

            return name in services
            # for ser in services:
            #    if ser in name:
            #        return True

            return False

        doc = self.latest_system_info
        found = []

        if self.IsDomainController():
            found.append("Domain Controller")

        for product in doc.get("data").get("Win32_Product", {}):
            service_name = eval(product.get("Name"))

            if not IsNameOfCriticalService(service_name):
                continue

            found.append(service_name)

        for service in doc.get("data").get("Win32_Service", {}):
            service_name = eval(service.get("Name"))

            if not IsNameOfCriticalService(service_name):
                continue

            if eval(service.get("State")) != "Running":
                continue

            found.append(service_name)

        return found

    @cache
    def IsCriticalServer(self):
        return len(self.GetCriticalServicesInstalled()) > 0

    @cache
    def GetUsernamesBySecret(self, secret):
        sam = self.GetLocalSecrets()

        names = set()

        for username, user_secret in sam.iteritems():
            if secret == user_secret:
                names.add(username)

        return names

    @cache
    def GetSidsBySecret(self, secret):
        usernames = self.GetUsernamesBySecret(secret)
        return set(map(self.GetSidByUsername, usernames))

    @cache
    def GetGroupSidByGroupName(self, group_name):
        doc = self.latest_system_info

        for group in doc.get('data').get("Win32_Group", {}):
            if eval(group.get("Name")) != group_name:
                continue

            if not is_group_sid_type(group.get("SIDType")):
                continue

            return eval(group.get("SID"))

        return None

    @cache
    def GetUsersByGroupSid(self, sid):
        doc = self.latest_system_info

        users = dict()

        for group_user in doc.get('data').get("Win32_GroupUser", {}):
            if eval(group_user.get("GroupComponent", {}).get("SID")) != sid:
                continue

            if not is_group_sid_type(group_user.get("GroupComponent", {}).get("SIDType")):
                continue

            if "PartComponent" not in group_user.keys():
                continue

            if type(group_user.get("PartComponent")) in (str, unicode):
                # PartComponent is an id to Win32_UserAccount table

                wmi_id = group_user.get("PartComponent")

                if "cimv2:Win32_UserAccount" not in wmi_id:
                    continue

                # u'\\\\WIN-BFA01FFQFLS\\root\\cimv2:Win32_UserAccount.Domain="MYDOMAIN",Name="WIN-BFA01FFQFLS$"'
                username = wmi_id.split('cimv2:Win32_UserAccount.Domain="')[1].split('",Name="')[0]
                domain = wmi_id.split('cimv2:Win32_UserAccount.Domain="')[1].split('",Name="')[1][:-1]

                sid = self.GetSidByUsername(username, domain)
                users[sid] = username

            else:
                if group_user.get("PartComponent", {}).get("SIDType") != SidTypeUser:
                    continue

                users[eval(group_user.get("PartComponent", {}).get("SID"))] = eval(group_user.get("PartComponent")
                                                                                   .get("Name"))

        return users

    @cache
    def GetDomainControllersMonkeyGuidByDomainName(self, domain_name):
        cur = mongo.db.telemetry.find(
            {"telem_type": "system_info_collection", "data.Win32_ComputerSystem.Domain": "u'%s'" % (domain_name,)})

        GUIDs = set()

        for doc in cur:
            if not Machine(doc.get("monkey_guid")).IsDomainController():
                continue

            GUIDs.add(doc.get("monkey_guid"))

        return GUIDs

    @cache
    def GetLocalAdmins(self):
        admins = self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Administrators"))

        # debug = self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Users"))
        # admins.update(debug)

        return admins

    @cache
    def GetLocalAdminSids(self):
        return set(self.GetLocalAdmins().keys())

    @cache
    def GetLocalSids(self):
        doc = self.latest_system_info

        SIDs = set()

        for user in doc.get('data').get("Win32_UserAccount", {}):
            if user.get("SIDType") != SidTypeUser:
                continue

            SIDs.add(eval(user.get("SID")))

        return SIDs

    @cache
    def GetLocalAdminNames(self):
        return set(self.GetLocalAdmins().values())

    @cache
    def GetSam(self):
        if not self.GetMimikatzOutput():
            return {}

        mimikatz = self.GetMimikatzOutput()

        if mimikatz.count("\n42.") != 2:
            return {}

        try:
            sam_users = mimikatz.split("\n42.")[1].split("\nSAMKey :")[1].split("\n\n")[1:]

            sam = {}

            for sam_user_txt in sam_users:
                sam_user = dict([map(unicode.strip, line.split(":")) for line in
                                 filter(lambda l: l.count(":") == 1, sam_user_txt.splitlines())])

                ntlm = sam_user.get("NTLM")
                if "[hashed secret]" not in ntlm:
                    continue

                sam[sam_user.get("User")] = ntlm.replace("[hashed secret]", "").strip()

            return sam

        except:
            return {}

    @cache
    def GetNtds(self):
        if not self.GetMimikatzOutput():
            return {}

        mimikatz = self.GetMimikatzOutput()

        if mimikatz.count("\n42.") != 2:
            return {}

        ntds_users = mimikatz.split("\n42.")[2].split("\nRID  :")[1:]
        ntds = {}

        for ntds_user_txt in ntds_users:
            user = ntds_user_txt.split("User :")[1].splitlines()[0].replace("User :", "").strip()
            ntlm = ntds_user_txt.split("* Primary\n    NTLM :")[1].splitlines()[0].replace("NTLM :", "").strip()
            ntlm = ntlm.replace("[hashed secret]", "").strip()

            if ntlm:
                ntds[user] = ntlm

        return ntds

    @cache
    def GetLocalSecrets(self):
        sam = self.GetSam()
        ntds = self.GetNtds()

        secrets = sam.copy()
        secrets.update(ntds)

        return secrets

    @cache
    def GetLocalAdminSecrets(self):
        return set(self.GetLocalAdminCreds().values())

    @cache
    def GetLocalAdminCreds(self):
        admin_names = self.GetLocalAdminNames()
        sam = self.GetLocalSecrets()

        admin_creds = dict()

        for username, secret in sam.iteritems():
            if username not in admin_names:
                continue

            admin_creds[username] = secret

        return admin_creds

    @cache
    def GetCachedSecrets(self):
        return set(self.GetCachedCreds().values())

    @cache
    def GetCachedCreds(self):
        doc = self.latest_system_info

        creds = dict()

        if not self.GetMimikatzOutput():
            return {}

        mimikatz = self.GetMimikatzOutput()

        for user in mimikatz.split("\n42.")[0].split("Authentication Id")[1:]:
            username = None
            secret = None

            for line in user.splitlines():
                if "User Name" in line:
                    username = line.split(":")[1].strip()

                if ("NTLM" in line or "Password" in line) and "[hashed secret]" in line:
                    secret = line.split(":")[1].replace("[hashed secret]", "").strip()

            if username and secret:
                creds[username] = secret

        return creds

    @cache
    def GetDomainControllers(self):
        domain_name = self.GetDomainName()
        DCs = self.GetDomainControllersMonkeyGuidByDomainName(domain_name)
        return map(Machine, DCs)

    @cache
    def GetDomainAdminsOfMachine(self):
        DCs = self.GetDomainControllers()

        domain_admins = set()

        for dc in DCs:
            domain_admins |= set(dc.GetUsersByGroupSid(self.GetGroupSidByGroupName("Domain Admins")).keys())

        return domain_admins

    @cache
    def GetAdmins(self):
        return self.GetLocalAdminSids() | self.GetDomainAdminsOfMachine()

    @cache
    def GetAdminNames(self):
        return set(map(lambda x: self.GetUsernameBySid(x), self.GetAdmins()))

    @cache
    def GetCachedSids(self):
        doc = self.latest_system_info

        SIDs = set()

        for username in doc.get('data').get("credentials", {}):
            sid = self.GetSidByUsername(username)

            if not sid:
                sid = "__USERNAME__" + username

            SIDs.add(sid)

        return SIDs

    @cache
    def GetCachedUsernames(self):
        doc = self.latest_system_info

        names = set()

        for username in doc.get('data').get("credentials", {}):
            names.add(username)

        return names


class PassTheHashReport(object):
    # _instance = None
    # def __new__(class_, *args, **kwargs):
    #    if not class_._instance:
    #        class_._instance = object.__new__(class_, *args, **kwargs)
    #
    #    return class_._instance

    def __init__(self):
        self.vertices = self.GetAllMachines()

        self.machines = map(Machine, self.vertices)
        self.edges = self.get_edges_by_sid()  # Useful for non-cached domain users
        #self.edges |= self.GetEdgesBySamHash()  # This will add edges based only on password hash without caring about username


    def GetAllMachines(self):
        cur = mongo.db.telemetry.find({"telem_type": "system_info_collection"})

        GUIDs = set()

        for doc in cur:
            GUIDs.add(doc.get("monkey_guid"))

        return GUIDs

    @cache
    def ReprSidList(self, sid_list, attacker, victim):
        users_list = []

        for sid in sid_list:
            username = Machine(victim).GetUsernameBySid(sid)

            # if not username:
            #    username = Machine(attacker).GetUsernameBySid(sid)

            if username:
                users_list.append(username)

        return users_list

    @cache
    def ReprSecretList(self, secret_list, victim):
        relevant_users_list = []

        for secret in secret_list:
            relevant_users_list.append(Machine(victim).GetUsernamesBySecret(secret))

        return relevant_users_list

    @staticmethod
    def __get_edge_label(attacker, victim):
        attacker_monkey = NodeService.get_monkey_by_guid(attacker)
        victim_monkey = NodeService.get_monkey_by_guid(victim)

        attacker_label = NodeService.get_monkey_label(attacker_monkey)
        victim_label = NodeService.get_monkey_label(victim_monkey)

        RIGHT_ARROW = u"\u2192"
        return "%s %s %s" % (attacker_label, RIGHT_ARROW, victim_label)

    def get_edges_by_sid(self):
        edges_list = []

        for attacker in self.vertices:
            cached = self.GetCachedSids(Machine(attacker))

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admins = Machine(victim).GetAdmins()

                if len(cached & admins) > 0:
                    relevant_users_list = self.ReprSidList(cached & admins, attacker, victim)
                    edges_list.append(
                        {
                            'from': attacker,
                            'to': victim,
                            'users': relevant_users_list,
                            '_label': PassTheHashReport.__get_edge_label(attacker, victim),
                            'id': str(uuid.uuid4())
                        })

        return edges_list

    @cache
    def GetEdgesBySamHash(self):
        edges = set()

        for attacker in self.vertices:
            cached_creds = set(Machine(attacker).GetCachedCreds().items())

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admin_creds = set(Machine(victim).GetLocalAdminCreds().items())

                if len(cached_creds & admin_creds) > 0:
                    label = self.ReprSecretList(set(dict(cached_creds & admin_creds).values()), victim)
                    edges.add((attacker, victim, label))

        return edges

    @cache
    def GetEdgesByUsername(self):
        edges = set()

        for attacker in self.vertices:
            cached = Machine(attacker).GetCachedUsernames()

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admins = Machine(victim).GetAdminNames()

                if len(cached & admins) > 0:
                    edges.add((attacker, victim))

        return edges

    @cache
    def Print(self):
        print map(lambda x: Machine(x).GetIp(), self.vertices)
        print map(lambda x: (Machine(x[0]).GetIp(), Machine(x[1]).GetIp()), self.edges)

    @cache
    def GetPossibleAttackCountBySid(self, sid):
        return len(self.GetPossibleAttacksBySid(sid))

    @cache
    def GetPossibleAttacksByAttacker(self, attacker):
        attacks = set()

        cached_creds = set(Machine(attacker).GetCachedCreds().items())

        for victim in self.vertices:
            if attacker == victim:
                continue

            admin_creds = set(Machine(victim).GetLocalAdminCreds().items())

            if len(cached_creds & admin_creds) > 0:
                curr_attacks = dict(cached_creds & admin_creds)
                attacks.add((attacker, victim, curr_attacks))

        return attacks

    @cache
    def GetPossibleAttacksBySid(self, sid):
        attacks = set()

        for attacker in self.vertices:
            tmp = self.GetPossibleAttacksByAttacker(attacker)

            for _, victim, curr_attacks in tmp:
                for username, secret in curr_attacks.iteritems():
                    if Machine(victim).GetSidByUsername(username) == sid:
                        attacks.add((attacker, victim))

        return attacks

    @cache
    def GetSecretBySid(self, sid):
        for m in self.machines:
            for user, user_secret in m.GetLocalSecrets().iteritems():
                if m.GetSidByUsername(user) == sid:
                    return user_secret

        return None

    @cache
    def GetVictimCountBySid(self, sid):
        return len(self.GetVictimsBySid(sid))

    @cache
    def GetVictimCountByMachine(self, attacker):
        return len(self.GetVictimsByAttacker(attacker))

    @cache
    def GetAttackCountBySecret(self, secret):
        return len(self.GetAttackersBySecret(secret))

    @cache
    def GetAllUsernames(self):
        names = set()

        for sid in self.GetAllSids():
            names.add(self.GetUsernameBySid(sid))

        return names

    @cache
    def GetAllSids(self):
        SIDs = set()

        for m in self.machines:
            SIDs |= m.GetLocalSids()

        return SIDs

    @cache
    def GetAllSecrets(self):
        secrets = set()

        for m in self.machines:
            for secret in m.GetLocalAdminSecrets():
                secrets.add(secret)

        return secrets

    @cache
    def GetUsernameBySid(self, sid):
        for m in self.machines:
            username = m.GetUsernameBySid(sid)

            if username:
                return username

        return None

    @cache
    def GetSidInfo(self, sid):
        for m in self.machines:
            info = m.GetSidInfo(sid)

            if info:
                return info

        return None

    @cache
    def GetSidsBySecret(self, secret):
        SIDs = set()

        for m in self.machines:
            SIDs |= m.GetSidsBySecret(secret)

        return SIDs

    @cache
    def GetAllDomainControllers(self):
        DCs = set()

        for m in self.machines:
            if m.IsDomainController():
                DCs.add(m)

        return DCs

    @cache
    def GetSidsByUsername(self, username):
        SIDs = set()

        for m in self.machines:
            sid = m.GetSidByUsername(username)
            if sid:
                SIDs.add(sid)

        return SIDs

    @cache
    def GetVictimsBySid(self, sid):
        machines = set()

        for m in self.machines:
            if sid in m.GetAdmins():
                machines.add(m)

        return machines

    @cache
    def GetVictimsBySecret(self, secret):
        machines = set()

        SIDs = self.GetSidsBySecret(secret)

        for m in self.machines:
            if len(SIDs & m.GetAdmins()) > 0:
                machines.add(m)

        return machines

    @cache
    def GetAttackersBySecret(self, secret):
        machines = set()

        for m in self.machines:
            if secret in m.GetCachedSecrets():
                machines.add(m)

        return machines

    @cache
    def GetAttackersByVictim(self, victim):
        if type(victim) != unicode:
            victim = victim.monkey_guid

        attackers = set()

        for edge in self.edges:
            if edge.get('to', None) == victim:
                attackers.add(edge.get('from', None))

        return set(map(Machine, attackers))

    @cache
    def GetAttackersBySid(self, sid):
        machines = set()

        for m in self.machines:
            if sid in self.GetCachedSids(m):
                machines.add(m)

        return machines

    @cache
    def GetVictimsByAttacker(self, attacker):
        if type(attacker) != unicode:
            attacker = attacker.monkey_guid

        victims = set()

        for atck, vic, _ in self.edges:
            if atck == attacker:
                victims.add(vic)

        return set(map(Machine, victims))

    @cache
    def GetInPathCountByVictim(self, victim, already_processed=None):
        if type(victim) != unicode:
            victim = victim.monkey_guid

        if not already_processed:
            already_processed = set([victim])

        count = 0

        for atck, vic, _ in self.edges:
            if atck == vic:
                continue

            if vic != victim:
                continue

            if atck in already_processed:
                continue

            count += 1

            already_processed.add(atck)
            count += self.GetInPathCountByVictim(atck, already_processed)

        return count

    @cache
    def GetCritialServers(self):
        machines = set()

        for m in self.machines:
            if m.IsCriticalServer():
                machines.add(m)

        return machines

    @cache
    def GetNonCritialServers(self):
        return set(self.machines) - self.GetCritialServers()

    @cache
    def GetCachedSids(self, m):
        sids = set()
        tmp = m.GetCachedSids()

        for sid in tmp:
            if sid.startswith("__USERNAME__"):

                s = self.GetSidsByUsername(sid[len("__USERNAME__"):])
                if len(s) == 1:
                    sids.add(s.pop())
                else:
                    sids.add(sid)

            else:
                sids.add(sid)

        return sids

    @cache
    def GetThreateningUsersByVictim(self, victim):
        threatening_users = set()

        for attacker in self.GetAttackersByVictim(victim):
            # For each attacker, get the cached users and check which of them is an admin on the victim
            threatening_users |= (self.GetCachedSids(attacker) & victim.GetAdmins())

        return threatening_users

    @cache
    def GetSharedAdmins(self, m):
        shared_admins = set()

        for other in self.machines:
            if m == other:
                continue

            shared_admins |= (m.GetLocalAdminSids() & other.GetLocalAdminSids())

        shared_admins -= m.GetDomainAdminsOfMachine()
        return shared_admins