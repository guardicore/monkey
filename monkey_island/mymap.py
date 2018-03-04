import hashlib
import binascii
from pymongo import MongoClient
db = MongoClient().monkeyisland

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
    
    def GetMimikatzOutput(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        output = set()
        
        for doc in cur:
            output.add(doc["data"]["mimikatz"])

        if len(output) == 1:
            return output.pop()

        return None
    
    def GetHostName(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        names = set()

        for doc in cur:
            for comp in doc["data"]["Win32_ComputerSystem"]:
                names.add(eval(comp["Name"]))

        if len(names) == 1:
            return names.pop()

        return None

    def GetIp(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        names = set()

        for doc in cur:
            for addr in doc["data"]["network_info"]["networks"]:
                return str(addr["addr"])

        return None

    def GetDomainName(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        names = set()

        for doc in cur:
            for comp in doc["data"]["Win32_ComputerSystem"]:
                names.add(eval(comp["Domain"]))

        if len(names) == 1:
            return names.pop()

        return None
        
    def GetDomainRole(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        roles = set()

        for doc in cur:
            for comp in doc["data"]["Win32_ComputerSystem"]:
                roles.add(comp["DomainRole"])

        if len(roles) == 1:
            return roles.pop()

        return None

    def GetSidByUsername(self, username):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid, "data.Win32_UserAccount.Name":"u'%s'" % (username,)})
        
        SIDs = set()

        for doc in cur:
            for user in doc["data"]["Win32_UserAccount"]:
                if eval(user["Name"]) != username:
                    continue

                SIDs.add(eval(user["SID"]))
        
        if len(SIDs) == 1:
            return SIDs.pop()
        
        return None

    def GetUsernameBySid(self, sid):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid, "data.Win32_UserAccount.SID":"u'%s'" % (sid,)})
        
        names = set()

        for doc in cur:
            for user in doc["data"]["Win32_UserAccount"]:
                if eval(user["SID"]) != sid:
                    continue

                names.add(eval(user["Name"]))
        
        if len(names) == 1:
            return names.pop()
        
        return None

    def GetGroupSidByGroupName(self, group_name):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid, "data.Win32_Group.Name":"u'%s'" % (group_name,)})
        SIDs = set()

        for doc in cur:
            for group in doc["data"]["Win32_Group"]:
                if eval(group["Name"]) != group_name:
                    continue

                SIDs.add(eval(group["SID"]))
        
        if len(SIDs) == 1:
            return SIDs.pop()
        
        return None

    def GetUsersByGroupSid(self, sid):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid, "data.Win32_GroupUser.GroupComponent.SID":"u'%s'" % (sid,)})

        users = dict()

        for doc in cur:
            for group_user in doc["data"]["Win32_GroupUser"]:
                if eval(group_user["GroupComponent"]["SID"]) != sid:
                    continue
                
                if "PartComponent" not in group_user.keys():
                    continue

                users[eval(group_user["PartComponent"]["SID"])] = eval(group_user["PartComponent"]["Name"])
        
        return users

    def GetDomainControllersMonkeyGuidByDomainName(self, domain_name):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "data.Win32_ComputerSystem.Domain":"u'%s'" % (domain_name,)})
        
        GUIDs = set()

        for doc in cur:
            for comp in doc["data"]["Win32_ComputerSystem"]:
                if ((comp["DomainRole"] != DsRole_RolePrimaryDomainController) and
                    (comp["DomainRole"] != DsRole_RoleBackupDomainController)):
                    continue

                GUIDs.add(doc["monkey_guid"])
        
        return GUIDs

    def GetLocalAdmins(self):
        return self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Administrators")).keys()

    def GetLocalAdminNames(self):
        return self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Administrators")).values()
        
    def GetLocalAdminSecrets(self):
        admin_names = self.GetLocalAdminNames()
        sam_users = str(self.GetMimikatzOutput()).split("\nSAMKey :")[1].split("\n\n")[1:]
        
        admin_secrets = set()
        
        for sam_user_txt in sam_users:
            sam_user = dict([map(str.strip, line.split(":")) for line in filter(lambda l: l.count(":") == 1, sam_user_txt.splitlines())])
            
            if sam_user["User"] not in admin_names:
                continue
            
            admin_secrets.add(sam_user["NTLM"].replace("[hashed secret]", "").strip())
        
        return admin_secrets
    
    def GetCachedSecrets(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        secrets = set()
        
        for doc in cur:
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

    def GetDomainAdminsOfMachine(self):
        domain_name = self.GetDomainName()
        DCs = self.GetDomainControllersMonkeyGuidByDomainName(domain_name)
        
        domain_admins = set()
        
        for dc_monkey_guid in DCs:
            domain_admins |= Machine(dc_monkey_guid).GetLocalAdmins()
        
        return domain_admins

    def GetAdmins(self):
        return self.GetLocalAdmins() | self.GetDomainAdminsOfMachine()
        
    def GetAdminNames(self):
        return set(map(lambda x: self.GetUsernameBySid(x), self.GetAdmins()))

    def GetCachedSids(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        SIDs = set()
        
        for doc in cur:
            for username in doc["data"]["credentials"]:
                SIDs.add(self.GetSidByUsername(username))
        
        return SIDs

    def GetCachedUsernames(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        SIDs = set()
        
        for doc in cur:
            for username in doc["data"]["credentials"]:
                SIDs.add(username)
        
        return SIDs

class PassTheHashMap(object):
    def __init__(self):
        self.vertices = self.GetAllMachines()
        self.edges = set()
        
        self.GenerateEdgesBySid()      # Useful for non-cached domain users
        self.GenerateEdgesBySamHash()  # This will add edges based only on password hash without caring about username
        
    def GetAllMachines(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection"})
        
        GUIDs = set()
        
        for doc in cur:
            GUIDs.add(doc["monkey_guid"])

        return GUIDs

    def GenerateEdgesBySid(self):
        for attacker in self.vertices:
            cached = Machine(attacker).GetCachedSids()

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admins = Machine(victim).GetAdmins()
                
                if len(cached & admins) > 0:
                    self.edges.add((attacker, victim))

    def GenerateEdgesBySamHash(self):
        for attacker in self.vertices:
            cached = Machine(attacker).GetCachedSecrets()

            for victim in self.vertices:
                if attacker == victim:
                    continue

                admins = Machine(victim).GetLocalAdminSecrets()
                
                if len(cached & admins) > 0:
                    self.edges.add((attacker, victim))

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

PassTheHashMap().Print()

#monkey_guid_island = 345051728334
#monkey_guid_c = 345051740363
#monkey_guid_d = 345051735830
#
#island = Machine(monkey_guid_island)
#c = Machine(monkey_guid_c)
#d = Machine(monkey_guid_d)
#
#assert str(island.GetIp()).endswith(".5")
#assert str(c.GetIp()).endswith(".203")
#assert str(d.GetIp()).endswith(".204")

#print "sam", island.GetLocalAdminSecrets()
#print "lsa", island.GetCachedSecrets()

#print "cached", c.GetCachedSids()
#print "admins", d.GetAdmins()
