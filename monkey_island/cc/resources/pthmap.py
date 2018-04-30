import hashlib
import binascii
from pymongo import MongoClient

class mongo(object):
    db = MongoClient().monkeyisland

#class PthMap(flask_restful.Resource):
class PthMap(object):
    #@jwt_required()
    def get(self, **kw):
        graph = PassTheHashMap()

        return \
            {
                "nodes": [{"id": x, "label": Machine(x).GetIp()} for x in graph.vertices],
                "edges": [{"id": str(s) + str(t), "from": s, "to": t, "label": label} for s, t, label in graph.edges]
            }

if not __name__ == "__main__":
    import flask_restful
    
    from cc.auth import jwt_required
    from cc.services.edge import EdgeService
    from cc.services.node import NodeService
    from cc.database import mongo
    
    PthMapOrig = PthMap
    
    class PthMap(flask_restful.Resource):
        @jwt_required()
        def get(self, **kw):
            return PthMapOrig.get(self, **kw)
    
DsRole_RoleStandaloneWorkstation = 0
DsRole_RoleMemberWorkstation = 1
DsRole_RoleStandaloneServer = 2
DsRole_RoleMemberServer = 3
DsRole_RoleBackupDomainController = 4
DsRole_RolePrimaryDomainController = 5

def myntlm(x):
    hash = hashlib.new('md4', x.encode('utf-16le')).digest()
    return str(binascii.hexlify(hash))

def cache(foo):
    def hash(o):
        if type(o) in (int, float, str, unicode):
            return o

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
            
        elif type(o) == PthMap:
            return "PthMapSingleton"
            
        elif type(o) == PassTheHashMap:
            return "PassTheHashMapSingleton"

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

        return foo._mycache_[hashed]

    return wrapper

class Machine(object):
    def __init__(self, monkey_guid):
        self.monkey_guid = str(monkey_guid)
        
        self.latest_system_info = mongo.db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid}).sort([("timestamp", -1)]).limit(1)
        
        if self.latest_system_info.count() > 0:
            self.latest_system_info = self.latest_system_info[0]
    
    @cache
    def GetMimikatzOutput(self):
        doc = self.latest_system_info
        
        if not doc:
            return None
        
        return doc["data"]["mimikatz"]
    
    @cache
    def GetHostName(self):
        doc = self.latest_system_info

        for comp in doc["data"]["Win32_ComputerSystem"]:
            return eval(comp["Name"])

        return None

    @cache
    def GetIp(self):
        doc = self.latest_system_info
        
        for addr in doc["data"]["network_info"]["networks"]:
            return str(addr["addr"])

        return None

    @cache
    def GetDomainName(self):
        doc = self.latest_system_info
        
        for comp in doc["data"]["Win32_ComputerSystem"]:
            return eval(comp["Domain"])

        return None
    
    @cache
    def GetDomainRole(self):
        doc = self.latest_system_info
        
        for comp in doc["data"]["Win32_ComputerSystem"]:
            return comp["DomainRole"]

        return None
    
    @cache
    def IsDomainController(self):
        return self.GetDomainRole() in (DsRole_RolePrimaryDomainController, DsRole_RoleBackupDomainController)

    @cache
    def GetSidByUsername(self, username):
        doc = self.latest_system_info

        for user in doc["data"]["Win32_UserAccount"]:
            if eval(user["Name"]) != username:
                continue

            return eval(user["SID"])

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
        
        return info["Domain"] + "\\" + info["Username"]
    
    @cache
    def GetSidInfo(self, sid):
        doc = self.latest_system_info

        for user in doc["data"]["Win32_UserAccount"]:
            if eval(user["SID"]) != sid:
                continue

            return { "Domain": eval(user["Domain"]),
                     "Username": eval(user["Name"]),
                     "Disabled": user["Disabled"] == "true",
                     "PasswordRequired": user["PasswordRequired"] == "true",
                     "PasswordExpires": user["PasswordExpires"] == "true", }
        
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
            
            for ser in services:
                if ser in name:
                    return True
            
            return False
    
        doc = self.latest_system_info
        found = []
        
        if self.IsDomainController():
            found.append("Domain Controller")

        for product in doc["data"]["Win32_Product"]:
            service_name = eval(product["Name"])
            
            if not IsNameOfCriticalService(service_name):
                continue
            
            found.append(service_name)

        for service in doc["data"]["Win32_Service"]:
            service_name = eval(service["Name"])
            
            if not IsNameOfCriticalService(service_name):
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

        for group in doc["data"]["Win32_Group"]:
            if eval(group["Name"]) != group_name:
                continue

            return eval(group["SID"])
        
        return None

    @cache
    def GetUsersByGroupSid(self, sid):
        doc = self.latest_system_info

        users = dict()
        
        for group_user in doc["data"]["Win32_GroupUser"]:
            if eval(group_user["GroupComponent"]["SID"]) != sid:
                continue
            
            if "PartComponent" not in group_user.keys():
                continue

            users[eval(group_user["PartComponent"]["SID"])] = eval(group_user["PartComponent"]["Name"])
        
        return users

    @cache
    def GetDomainControllersMonkeyGuidByDomainName(self, domain_name):
        cur = mongo.db.telemetry.find({"telem_type":"system_info_collection", "data.Win32_ComputerSystem.Domain":"u'%s'" % (domain_name,)})
        
        GUIDs = set()

        for doc in cur:
            if not Machine(doc["monkey_guid"]).IsDomainController():
                continue

            GUIDs.add(doc["monkey_guid"])
        
        return GUIDs

    @cache
    def GetLocalAdmins(self):
        admins = self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Administrators"))
        
        #debug = self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Users"))
        #admins.update(debug)
        
        return admins
        
    @cache
    def GetLocalAdminSids(self):
        return set(self.GetLocalAdmins().keys())
    
    @cache
    def GetLocalSids(self):
        doc = self.latest_system_info
        
        SIDs = set()
    
        for user in doc["data"]["Win32_UserAccount"]:
            SIDs.add(eval(user["SID"]))
        
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
                sam_user = dict([map(unicode.strip, line.split(":")) for line in filter(lambda l: l.count(":") == 1, sam_user_txt.splitlines())])
                
                ntlm = sam_user["NTLM"]
                if "[hashed secret]" not in ntlm:
                    continue

                sam[sam_user["User"]] = ntlm.replace("[hashed secret]", "").strip()

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
            domain_admins |= dc.GetLocalAdminSids()
        
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
        
        for username in doc["data"]["credentials"]:
            sid = self.GetSidByUsername(username)
            
            if not sid:
                sid = "__USERNAME__" + username

            SIDs.add(sid)
        
        return SIDs

    @cache
    def GetCachedUsernames(self):
        doc = self.latest_system_info
        
        names = set()
        
        for username in doc["data"]["credentials"]:
            names.add(username)
        
        return names

class PassTheHashMap(object):
    def __init__(self):
        self.vertices = self.GetAllMachines()
        
        self.edges = set()
        self.machines = map(Machine, self.vertices)

        self.GenerateEdgesBySid()      # Useful for non-cached domain users
        self.GenerateEdgesBySamHash()  # This will add edges based only on password hash without caring about username

    @cache
    def GetAllMachines(self):
        cur = mongo.db.telemetry.find({"telem_type":"system_info_collection"})
        
        GUIDs = set()
        
        for doc in cur:
            GUIDs.add(doc["monkey_guid"])

        return GUIDs

    @cache
    def ReprSidList(self, sid_list, attacker, victim):
        label = set()
        
        for sid in sid_list:
            username = Machine(victim).GetUsernameBySid(sid)
            
            #if not username:
            #    username = Machine(attacker).GetUsernameBySid(sid)
            
            if username:
                label.add(username)
        
        return ",\n".join(label)

    @cache
    def ReprSecretList(self, secret_list, victim):
        label = set()
        
        for secret in secret_list:
            label |= Machine(victim).GetUsernamesBySecret(secret)
        
        return ",\n".join(label)

    @cache
    def GenerateEdgesBySid(self):
        for attacker in self.vertices:
            cached = Machine(attacker).GetCachedSids()

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admins = Machine(victim).GetAdmins()

                if len(cached & admins) > 0:
                    label = self.ReprSidList(cached & admins, attacker, victim)
                    self.edges.add((attacker, victim, label))

    @cache
    def GenerateEdgesBySamHash(self):
        for attacker in self.vertices:
            cached_creds = set(Machine(attacker).GetCachedCreds().items())

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admin_creds = set(Machine(victim).GetLocalAdminCreds().items())
                
                if len(cached_creds & admin_creds) > 0:
                    label = self.ReprSecretList(set(dict(cached_creds & admin_creds).values()), victim)
                    self.edges.add((attacker, victim, label))

    @cache
    def GenerateEdgesByUsername(self):
        for attacker in self.vertices:
            cached = Machine(attacker).GetCachedUsernames()

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admins = Machine(victim).GetAdminNames()
                
                if len(cached & admins) > 0:
                    self.edges.add((attacker, victim))

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

        for atck, vic, _ in self.edges:
            if vic == victim:
                attackers.add(atck)
        
        return set(map(Machine, attackers))

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
    def GetThreateningUsersByVictim(self, victim):
        threatening_users = set()
        
        for attacker in self.GetAttackersByVictim(victim):
            threatening_users |= (attacker.GetCachedSids() & victim.GetAdmins())

        return threatening_users
        
def main():
    pth = PassTheHashMap()

    print "<h1>Pass The Hash Report</h1>"
    
    print "<h2>Duplicated Passwords</h2>"
    print "<h3>How many users share each secret?</h3>"
    
    dups = dict(map(lambda x: (x, len(pth.GetSidsBySecret(x))), pth.GetAllSecrets()))
    
    print """<table>"""
    print """<tr><th>Secret</th><th>User Count</th><th>Users That Share This Password</th></tr>"""
    for secret, count in sorted(dups.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if count <= 1:
            continue
        print """<tr><td><a href="#{secret}">{secret}</a></td><td>{count}</td>""".format(secret=secret, count=count)
        print """<td><ul>"""
        for sid in pth.GetSidsBySecret(secret):
            print """<li><a href="#{sid}">{username}</a></li>""".format(sid=sid, username=pth.GetUsernameBySid(sid))
        print """</ul></td></tr>"""
    print """</table>"""
    
    
    
    print "<h2>Strong Users That Threat Critical Servers</h2>"
    print "<h3>Administrators of critical servers that we could find thier secret cached somewhere</h3>"
    
    threatening = dict(map(lambda x: (x, len(pth.GetThreateningUsersByVictim(x))), pth.GetCritialServers()))
    
    print """<table>"""
    print """<tr><th>Critical Server</th><th>Hostname</th><th>Domain</th><th>Threatening User Count</th><th>Threatening Users</th></tr>"""
    for m, count in sorted(threatening.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if count <= 0:
            continue
        print """<tr><td><a href="#{ip}">{ip}</a></td><td>{hostname}</td><td>{domain}</td><td>{count}</td>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), count=count)
        print """<td><ul>"""
        
        for sid in pth.GetThreateningUsersByVictim(m):
            print """<li><a href="#{sid}">{username}</a></li>""".format(sid=sid, username=pth.GetUsernameBySid(sid))

        print """</ul></td></tr>"""
    print """</table>"""
    
    
    print "<h2>Strong Users That Threat NonCritical Servers</h2>"
    print "<h3>Administrators of non-critical servers that we could find thier secret cached somewhere</h3>"
    
    threatening = dict(map(lambda x: (x, len(pth.GetThreateningUsersByVictim(x))), pth.GetNonCritialServers()))
    
    print """<table>"""
    print """<tr><th>Critical Server</th><th>Hostname</th><th>Domain</th><th>Threatening User Count</th><th>Threatening Users</th></tr>"""
    for m, count in sorted(threatening.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if count <= 0:
            continue
        print """<tr><td><a href="#{ip}">{ip}</a></td><td>{hostname}</td><td>{domain}</td><td>{count}</td>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), count=count)
        print """<td><ul>"""
        
        for sid in pth.GetThreateningUsersByVictim(m):
            print """<li><a href="#{sid}">{username}</a></li>""".format(sid=sid, username=pth.GetUsernameBySid(sid))

        print """</ul></td></tr>"""
    print """</table>"""

    
    print "<h2>Cached Passwords</h2>"
    print "<h3>On how many machines each secret is cached (possible attacker count)?</h3>"
    cache_counts = dict(map(lambda x: (x, pth.GetAttackCountBySecret(x)), pth.GetAllSecrets()))
    
    print """<table>"""
    print """<tr><th>Secret</th><th>Machine Count</th></tr>"""
    for secret, count in sorted(cache_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if count <= 0:
            continue
        print """<tr><td><a href="#{secret}">{secret}</a></td><td>{count}</td>""".format(secret=secret, count=count)
    print """</table>"""
    
    print "<h2>User's Creds</h2>"
    print "<h3>To how many machines each user is able to connect with admin rights</h3>"
    attackable_counts = dict(map(lambda x: (x, pth.GetVictimCountBySid(x)), pth.GetAllSids()))
    
    print """<table>"""
    print """<tr><th>SID</th><th>Username</th><th>Machine Count</th></tr>"""
    for sid, count in sorted(attackable_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if count <= 1:
            continue
        print """<tr><td><a href="#{sid}">{sid}</a></td><td>{username}</td><td>{count}</td>""".format(sid=sid, username=pth.GetUsernameBySid(sid), count=count)
    print """</table>"""
    
    print "<h2>Actual Possible Attacks By SID</h2>"
    print "<h3>How many attacks possible using each SID (aka len(attacker->victim pairs))</h3>"
    possible_attacks_by_sid = dict(map(lambda x: (x, pth.GetPossibleAttackCountBySid(x)), pth.GetAllSids()))
    
    print """<table>"""
    print """<tr><th>SID</th><th>Username</th><th>Machine Count</th></tr>"""
    for sid, count in sorted(possible_attacks_by_sid.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if count <= 1:
            continue
        print """<tr><td><a href="#{sid}">{sid}</a></td><td>{username}</td><td>{count}</td>""".format(sid=sid, username=pth.GetUsernameBySid(sid), count=count)
    print """</table>"""
    
    print "<h2>Machine's Creds</h2>"
    print "<h3>To how many machines each machine is able to directly connect with admin rights?</h3>"
    attackable_counts = dict(map(lambda m: (m, pth.GetVictimCountByMachine(m)), pth.machines))
    
    print """<table>"""
    print """<tr><th>Attacker Ip</th><th>Attacker Hostname</th><th>Domain Name</th><th>Victim Machine Count</th></tr>"""
    for m, count in sorted(attackable_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if count <= 1:
            continue
        print """<tr><td><a href="#{ip}">{ip}</a></td><td>{hostname}</td><td>{domain}</td><td>{count}</td>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), count=count)
    print """</table>"""
    
    print "<h2>Domain Controllers</h2>"
    print "<h3>List of domain controllers (we count them as critical points, so they are listed here)</h3>"
    DCs = dict(map(lambda m: (m, pth.GetInPathCountByVictim(m)), pth.GetAllDomainControllers()))
    
    print """<table>"""
    print """<tr><th>DC Ip</th><th>DC Hostname</th><th>Domain Name</th><th>In-Path Count</th></tr>"""
    for m, path_count in sorted(DCs.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print """<tr><td><a href="#{ip}">{ip}</a></td><td><a href="#{ip}">{hostname}</a></td><td>{domain}</td><td>{path_count}</td></tr>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), path_count=path_count)
    print """</table>"""
    
    print "<h2>Most Vulnerable Machines</h2>"
    print "<h3>List all machines in the network sorted by the potincial to attack them</h3>"
    all_machines = dict(map(lambda m: (m, pth.GetInPathCountByVictim(m)), pth.machines))
    
    print """<table>"""
    print """<tr><th>Ip</th><th>Hostname</th><th>Domain Name</th><th>In-Path Count</th></tr>"""
    for m, path_count in sorted(all_machines.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if count <= 0:
            continue
        print """<tr><td><a href="#{ip}">{ip}</a></td><td><a href="#{ip}">{hostname}</a></td><td>{domain}</td><td>{path_count}</td></tr>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), path_count=path_count)
    print """</table>"""
    
    print "<h2>Critical Servers</h2>"
    print "<h3>List of all machines identified as critical servers</h3>"
    critical_servers = pth.GetCritialServers()
    
    print """<table>"""
    print """<tr><th>Ip</th><th>Hostname</th><th>Domain Name</th></tr>"""
    for m in critical_servers:
        print """<tr><td><a href="#{ip}">{ip}</a></td><td><a href="#{ip}">{hostname}</a></td><td>{domain}</td></tr>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName())
    print """</table>"""
    
    print "<hr />"
    
    for m in pth.machines:
        print """<a name="{ip}"><h2>Machine '{ip}'</h2></a>
                 <h3>Hostname '{hostname}'</h3>""".format(ip=m.GetIp(), hostname=m.GetHostName())
     
        print """<h3>Cached SIDs</h3>"""
        print """<h4>SIDs cached on this machine</h4>"""
        print """<ul>"""
        for sid in m.GetCachedSids():
            if sid.startswith("__USERNAME__"):
                sids = pth.GetSidsByUsername(sid[len("__USERNAME__"):])
                if len(sids) == 1:
                    sid = sids.pop()

            print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=pth.GetUsernameBySid(sid), sid=sid)
        print """</ul>"""
        
        print """<h3>Possible Attackers</h3>"""
        print """<h4>Machines that can attack this machine</h4>"""
        print """<ul>"""
        for attacker in pth.GetAttackersByVictim(m):
            print """<li><a href="#{ip}">{ip} ({hostname})</a></li>""".format(ip=attacker.GetIp(), hostname=attacker.GetHostName())
        print """</ul>"""
            
        
        print """<h3>Admins</h3>"""
        print """<h4>Users that have admin rights on this machine</h4>"""
        print """<ul>"""
        for sid in m.GetAdmins():
            print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=m.GetUsernameBySid(sid), sid=sid)
        print """</ul>"""
        
        print """<h3>Installed Critical Services</h3>"""
        print """<h4>List of crtical services found installed on machine</h4>"""
        print """<ul>"""
        for service_name in m.GetCriticalServicesInstalled():
            print """<li>{service_name}</li>""".format(service_name=service_name)
        print """</ul>"""
        
        

    print "<hr />"
    
    for username in pth.GetAllUsernames():
        print """<a name="{username}"><h2>User '{username}'</h2></a>""".format(username=username)
        
        print """<h3>Matching SIDs</h3>"""
        print """<ul>"""
        for sid in pth.GetSidsByUsername(username):
            print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=pth.GetUsernameBySid(sid), sid=sid)
        print """</ul>"""

    print "<hr />"
    
    for sid in pth.GetAllSids():
        print """<a name="{sid}"><h2>SID '{sid}'</h2></a>
                <h3>Username: '<a href="#{username}">{username}</a>'</h3>
                <h3>Domain: {domain}</h3>
                <h3>Secret: '<a href="#{secret}">{secret}</a>'</h3>
              """.format(username=pth.GetUsernameBySid(sid), sid=sid, secret=pth.GetSecretBySid(sid), domain=pth.GetSidInfo(sid)["Domain"])
        
        print """<h3>Attackable Machines</h3>"""
        print """<ul>"""
        for m in pth.GetVictimsBySid(sid):
            print """<li><a href="#{ip}">{ip} ({hostname})</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        print """</ul>"""

    for secret in pth.GetAllSecrets():
        print """<a name="{secret}"><h2>Secret '{secret}'</h2></a>""".format(secret=secret)
        
        print """<h3>SIDs that use that secret</h3>"""
        print """<ul>"""
        for sid in pth.GetSidsBySecret(secret):
            print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=pth.GetUsernameBySid(sid), sid=sid)
        print """</ul>"""
        
        print """<h3>Attackable Machines with that secret</h3>"""
        print """<ul>"""
        for m in pth.GetVictimsBySecret(secret):
            print """<li><a href="#{ip}">{hostname}</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        print """</ul>"""
        
        print """<h3>Machines that have this secret cached and can use it to attack other machines</h3>"""
        print """<ul>"""
        for m in pth.GetAttackersBySecret(secret):
            print """<li><a href="#{ip}">{hostname}</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        print """</ul>"""
        
    
if __name__ == "__main__":
    main()