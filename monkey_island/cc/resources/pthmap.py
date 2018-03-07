#import flask_restful
#
#from cc.auth import jwt_required
#from cc.services.edge import EdgeService
#from cc.services.node import NodeService
#from cc.database import mongo

import hashlib
import binascii
from pymongo import MongoClient

class PthMap(flask_restful.Resource):
    @jwt_required()
    def get(self, **kw):
        graph = PassTheHashMap()

        return \
            {
                "nodes": [{"id": x, "label": Machine(x).GetIp()} for x in graph.vertices],
                "edges": [{"id": str(s) + str(t), "from": s, "to": t, "label": label} for s, t, label in graph.edges]
            }

DsRole_RoleStandaloneWorkstation = 0
DsRole_RoleMemberWorkstation = 1
DsRole_RoleStandaloneServer = 2
DsRole_RoleMemberServer = 3
DsRole_RoleBackupDomainController = 4
DsRole_RolePrimaryDomainController = 5

def myntlm(x):
    hash = hashlib.new('md4', x.encode('utf-16le')).digest()
    return str(binascii.hexlify(hash))

class Machine(object):
    def __init__(self, monkey_guid):
        self.monkey_guid = str(monkey_guid)
        
        self.latest_system_info = mongo.db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid}).sort([("timestamp", 1)]).limit(1)
        
        if self.latest_system_info.count() > 0:
            self.latest_system_info = self.latest_system_info[0]
    
    def GetMimikatzOutput(self):
        doc = self.latest_system_info
        
        if not doc:
            return None
        
        return doc["data"]["mimikatz"]
    
    def GetHostName(self):
        doc = self.latest_system_info

        for comp in doc["data"]["Win32_ComputerSystem"]:
            return eval(comp["Name"])

        return None

    def GetIp(self):
        doc = self.latest_system_info
        
        for addr in doc["data"]["network_info"]["networks"]:
            return str(addr["addr"])

        return None

    def GetDomainName(self):
        doc = self.latest_system_info
        
        for comp in doc["data"]["Win32_ComputerSystem"]:
            return eval(comp["Domain"])

        return None
        
    def GetDomainRole(self):
        doc = self.latest_system_info
        
        for comp in doc["data"]["Win32_ComputerSystem"]:
            return comp["DomainRole"]

        return None
    
    def IsDomainController(self):
        return self.GetDomainRole() in (DsRole_RolePrimaryDomainController, DsRole_RoleBackupDomainController)

    def GetSidByUsername(self, username):
        doc = self.latest_system_info

        for user in doc["data"]["Win32_UserAccount"]:
            if eval(user["Name"]) != username:
                continue

            return eval(user["SID"])
        
        return None

    def GetUsernameBySid(self, sid):
        doc = self.latest_system_info

        for user in doc["data"]["Win32_UserAccount"]:
            if eval(user["SID"]) != sid:
                continue

            return eval(user["Name"])
        
        if not self.IsDomainController():
            for dc in self.GetDomainControllers():
                username = dc.GetUsernameBySid(sid)

                if username != None:
                    return username
        
        return None
        
    def GetUsernameBySecret(self, secret):
        sam = self.GetLocalSecrets()
        
        for user, user_secret in sam.iteritems():
            if secret == user_secret:
                return user

        return None

    def GetSidBySecret(self, secret):
        username = self.GetUsernameBySecret(secret)
        return self.GetSidByUsername(username)

    def GetGroupSidByGroupName(self, group_name):
        doc = self.latest_system_info

        for group in doc["data"]["Win32_Group"]:
            if eval(group["Name"]) != group_name:
                continue

            return eval(group["SID"])
        
        return None

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

    def GetDomainControllersMonkeyGuidByDomainName(self, domain_name):
        cur = mongo.db.telemetry.find({"telem_type":"system_info_collection", "data.Win32_ComputerSystem.Domain":"u'%s'" % (domain_name,)})
        
        GUIDs = set()

        for doc in cur:
            if not Machine(doc["monkey_guid"]).IsDomainController():
                continue

            GUIDs.add(doc["monkey_guid"])
        
        return GUIDs

    def GetLocalAdmins(self):
        return set(self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Administrators")).keys())
    
    def GetLocalSids(self):
        doc = self.latest_system_info
        
        SIDs = set()
    
        for user in doc["data"]["Win32_UserAccount"]:
            SIDs.add(eval(user["SID"]))
        
        return SIDs

    def GetLocalAdminNames(self):
        return set(self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Administrators")).values())
        
    def GetSam(self):
        if not self.GetMimikatzOutput():
            return {}
    
        mimikatz = self.GetMimikatzOutput()

        if mimikatz.count("\n42.") != 2:
            return {}

        sam_users = mimikatz.split("\n42.")[1].split("\nSAMKey :")[1].split("\n\n")[1:]

        sam = {}
        
        for sam_user_txt in sam_users:
            sam_user = dict([map(unicode.strip, line.split(":")) for line in filter(lambda l: l.count(":") == 1, sam_user_txt.splitlines())])
            sam[sam_user["User"]] = sam_user["NTLM"].replace("[hashed secret]", "").strip()
        
        return sam
    
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
    
    def GetLocalSecrets(self):
        sam = self.GetSam()
        ntds = self.GetNtds()
        
        secrets = sam.copy()
        secrets.update(ntds)
        
        return secrets

    def GetLocalAdminSecrets(self):
        admin_names = self.GetLocalAdminNames()
        sam = self.GetLocalSecrets()
        
        admin_secrets = set()
        
        for user, secret in sam.iteritems():
            if user not in admin_names:
                continue
            
            admin_secrets.add(secret)

        return admin_secrets
    
    def GetCachedSecrets(self):
        doc = self.latest_system_info
        
        secrets = set()
        
        for username in doc["data"]["credentials"]:
            user = doc["data"]["credentials"][username]
            
            if "password" in user.keys():
                ntlm = myntlm(str(user["password"]))
            elif "ntlm_hash" in user.keys():
                ntlm = str(user["ntlm_hash"])
            else:
                continue

            secret = hashlib.md5(ntlm.decode("hex")).hexdigest()
            secrets.add(secret)

        return secrets
    
    def GetDomainControllers(self):
        domain_name = self.GetDomainName()
        DCs = self.GetDomainControllersMonkeyGuidByDomainName(domain_name)
        return map(Machine, DCs)

    def GetDomainAdminsOfMachine(self):
        DCs = self.GetDomainControllers()
        
        domain_admins = set()
        
        for dc in DCs:
            domain_admins |= dc.GetLocalAdmins()
        
        return domain_admins

    def GetAdmins(self):
        return self.GetLocalAdmins() | self.GetDomainAdminsOfMachine()
        
    def GetAdminNames(self):
        return set(map(lambda x: self.GetUsernameBySid(x), self.GetAdmins()))

    def GetCachedSids(self):
        doc = self.latest_system_info
        
        SIDs = set()
        
        for username in doc["data"]["credentials"]:
            SIDs.add(self.GetSidByUsername(username))
        
        return SIDs

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
        
        self.GenerateEdgesBySid()      # Useful for non-cached domain users
        self.GenerateEdgesBySamHash()  # This will add edges based only on password hash without caring about username
        
    def GetAllMachines(self):
        cur = mongo.db.telemetry.find({"telem_type":"system_info_collection"})
        
        GUIDs = set()
        
        for doc in cur:
            GUIDs.add(doc["monkey_guid"])

        return GUIDs
        
    def ReprSidList(self, sid_list, attacker, victim):
        label = set()
        
        for sid in sid_list:
            username = Machine(victim).GetUsernameBySid(sid)
            
            #if not username:
            #    username = Machine(attacker).GetUsernameBySid(sid)
            
            if username:
                label.add(username)
        
        return ",\n".join(label)

    def ReprSecretList(self, secret_list, victim):
        label = set()
        
        for secret in secret_list:
            username = Machine(victim).GetUsernameBySecret(secret)
            
            if username:
                label.add(username)
        
        return ",\n".join(label)

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

    def GenerateEdgesBySamHash(self):
        for attacker in self.vertices:
            cached = Machine(attacker).GetCachedSecrets()

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admins = Machine(victim).GetLocalAdminSecrets()
                
                if len(cached & admins) > 0:
                    label = self.ReprSecretList(cached & admins, victim)
                    self.edges.add((attacker, victim, label))

    def GenerateEdgesByUsername(self):
        for attacker in self.vertices:
            cached = Machine(attacker).GetCachedUsernames()

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admins = Machine(victim).GetAdminNames()
                
                if len(cached & admins) > 0:
                    self.edges.add((attacker, victim))

    def Print(self):
        print map(lambda x: Machine(x).GetIp(), self.vertices)
        print map(lambda x: (Machine(x[0]).GetIp(), Machine(x[1]).GetIp()), self.edges)
    
    def GetSecretBySid(self, sid):
        for m in self.vertices:
            for user, user_secret in m.GetLocalSecrets():
                if m.GetSidByUsername(user) == sid:
                    return user_secret
        
        return None
    
    def GetAttackableMachineCountBySid(self, sid):
        count = 0
        
        for m in self.vertices:
            if sid in m.GetLocalAdmins():
                count += 1

        return count

    def GetAttackableMachineCountByMachine(self, attacker):
        count = 0
        
        for secret in attack.GetCachedSecrets():
            count += len(m.GetAttackableMachinesBySecret(secret))

        return count
    
    def GetSecretCacheCount(self, secret):
        count = 0
        
        for m in self.vertices:
            if secret in m.GetCachedSecrets():
                count += 1
        
        return count
    
    def GetAllUsernames(self):
        names = set()
        
        for sid in self.GetAllSids():
            names.add(self.GetUsernameBySid(sid))
        
        return names

    def GetAllSids(self):
        SIDs = set()
        
        for m in self.vertices:
            SIDs |= m.GetLocalSids()
        
        return SIDs

    def GetAllSecrets(self):
        secrets = set()
        
        for m in self.vertices:
            for secret in m.GetLocalAdminSecrets():
                secret.add(secret)
                #secrets[secret]["cache_count"] = self.GetSecretCacheCount(secret)
                #secrets[secret]["sid_count"] = len(self.GetSidsBySecret(secret))
        
        return secrets
    
    def GetUsernameBySid(self, sid):
        for m in self.vertices:
            username = m.GetUsernameBySid(sid)
            
            if username:
                return username
        
        return None
    
    def GetSidsBySecret(self, secret):
        SIDs = set()
        
        for m in self.vertices:
            SIDs.add(m.GetSidBySecret(secret))
        
        return SIDs
    
    def GetAllDomainControllers(self):
        DCs = set()
        
        for m in self.vertices:
            if m.IsDomainController():
                DCs.add(m)

    def GetSidsByUsername(self, username):
        doc = self.latest_system_info

        SIDs = set()
        
        for m in self.vertices:
            sid = m.GetSidByUsername(username)
            if sid:
                SIDs.add(sid)
        
        return SIDs
    
    def GetAttackableMachinesBySid(self, sid):
        machines = set()

        for m in self.vertices:
            if sid in m.GetAdmins():
                machines.add(m)

        return machines

    def GetAttackableMachinesBySecret(self, secret):
        machines = set()

        SIDs = self.GetSidsBySecret(secret)

        for m in self.vertices:
            if len(SIDs & m.GetAdmins()) > 0:
                machines.add(m)

        return machines

    def GetAttackersBySecret(self, secret):
        machines = set()
        
        for m in self.vertices:
            if secret in m.GetCachedSecrets():
                machines.add(m)

        return machines
    
    def GetAttackersByVictim(self, victim):
        attackers = set()
    
        for atck, vic in self.edge:
            if vic == victim:
                attackers.add(atck)
        
        return attackers

def main():
    pth = PassTheHashMap()

    print "<h1>Pass The Hash Report</h1>"
    
    print "<h2>Duplicated Passwords</h2>"
    print "<h3>How many users share each secret?</h3>"
    dups = dict(map(lambda x: (x, len(self.GetSidsBySecret(x))), pth.GetAllSecrets()))
    
    print """<talbe>"""
    print """<tr><th>Secret</th><th>User Count</th></tr>"""
    for secret, count in sorted(dups.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print """<tr><td>{secret}</td><td>{count}</td>""".format(secret=secret, count=count)
    print """</talbe>"""
    
    print "<h2>Cached Passwords</h2>"
    print "<h3>On how many machines each secret is cached?</h3>"
    cache_counts = dict(map(lambda x: (x, self.GetSecretCacheCount(x)), pth.GetAllSecrets()))
    
    print """<talbe>"""
    print """<tr><th>Secret</th><th>Machine Count</th></tr>"""
    for secret, count in sorted(cache_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print """<tr><td>{secret}</td><td>{count}</td>""".format(secret=secret, count=count)
    print """</talbe>"""
    
    print "<h2>User's Creds</h2>"
    print "<h3>To how many machines each user is able to connect with admin rights?</h3>"
    attackable_counts = dict(map(lambda x: (x, self.GetAttackableMachineCountBySid(x)), pth.GetAllSids()))
    
    print """<talbe>"""
    print """<tr><th>SID</th><th>Username</th><th>Machine Count</th></tr>"""
    for sid, count in sorted(attackable_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print """<tr><td>{sid}</td><td>{username}</td><td>{count}</td>""".format(sid=sid, username=pth.GetUsernameBySid(sid), count=count)
    print """</talbe>"""
    
    print "<h2>Machine's Creds</h2>"
    print "<h3>To how many machines each machine is able to directly connect with admin rights?</h3>"
    attackable_counts = dict(map(lambda m: (m, pth.GetAttackableMachineCountByMachine(m)), pth.vertices))
    
    print """<talbe>"""
    print """<tr><th>Attacker Ip</th><th>Attacker Hostname</th><th>Domain Name</th><th>Victim Machine Count</th></tr>"""
    for m, count in sorted(attackable_counts.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print """<tr><td>{ip}</td><td>{hostname}</td><td>{domain}</td><td>{count}</td>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName(), count=count)
    print """</talbe>"""
    
    print "<h2>Domain Controllers</h2>"
    print "<h3>List of domain controllers (we count them as critical points, so they are listed here)</h3>"
    DCs = pth.GetAllDomainControllers()
    
    print """<talbe>"""
    print """<tr><th>DC Ip</th><th>DC Hostname</th><th>Domain Name</th></tr>"""
    for m in DCs:
        print """<tr><td><a href="#{ip}">{ip}</a></td><td><a href="#{ip}">{hostname}</a></td><td>{domain}</td>""".format(ip=m.GetIp(), hostname=m.GetHostName(), domain=m.GetDomainName())
    print """</talbe>"""
    
    print "<hr />"
    
    for m in pth.vertices:
        print """<a name="{ip}"><h2>Machine '{ip}'</h2></a>
                 <h3>Hostname '{hostname}'</h3>""".format{ip=m.GetIp(), hostname=m.GetHostName()}
     
        print """<h3>Cached SIDs</h3>"""
        print """<h4>SIDs cached on this machine</h4>"""
        print """<ul>"""
        for sid in m.GetCachedSids():
            print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=m.GetUsernameBySid(sid), sid=sid)
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

    print "<hr />"
    
    for username in pth.GetAllUsernames():
        print """<a name="{username}"><h2>User '{username}'</h2></a>""".format(username=username)
        
        print """<h3>Matching SIDs</h3>"""
        print """<ul>"""
        for sid in pth.GetSidsByUsername(username)
            print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=m.GetUsernameBySid(sid), sid=sid)
        print """</ul>"""

    print "<hr />"
    
    for sid in pth.GetAllSids():
        print """<a name="{sid}"><h2>SID '{sid}'</h2></a>
                <a href="#{username}"><h3>Username: '{username}'</h3></a>
                <a href="#{secret}"><h3>Secret: '{secret}'</h3></a>
              """.format(username=pth.GetUsernameBySid(sid), sid=sid, secret=pth.GetSecretBySid(sid))
        
        print """<h3>Attackable Machines</h3>"""
        print """<ul>"""
        for m in pth.GetAttackableMachinesBySid(sid)
            print """<li><a href="#{ip}">{ip} ({hostname})</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        print """</ul>"""

    for secret in pth.GetAllSecrets():
        print """<a name="{secret}"><h2>Secret '{secret}'</h2></a>""".format(secret=secret)
        
        print """<h3>SIDs that use that secret</h3>"""
        print """<ul>"""
        for sid in pth.GetSidsBySecret(secret):
            print """<li><a href="#{sid}">{username} ({sid})</a></li>""".format(username=m.GetUsernameBySid(sid), sid=sid)
        print """</ul>"""
        
        print """<h3>Attackable Machines with that secret</h3>"""
        print """<ul>"""
        for m in pth.GetAttackableMachinesBySecret(secret):
            print """<li><a href="#{ip}">{hostname}</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        print """</ul>"""
        
        print """<h3>Machines that have this secret cached and can use it to attack other machines</h3>"""
        print """<ul>"""
        for m in pth.GetAttackersBySecret(secret):
            print """<li><a href="#{ip}">{hostname}</a></li>""".format(ip=m.GetIp(), hostname=m.GetHostName())
        print """</ul>"""
        
    
if __name__ == "__main__":
    main()