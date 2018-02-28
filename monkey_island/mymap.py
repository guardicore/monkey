from pymongo import MongoClient
db = MongoClient().monkeyisland

DsRole_RoleStandaloneWorkstation = 0
DsRole_RoleMemberWorkstation = 1
DsRole_RoleStandaloneServer = 2
DsRole_RoleMemberServer = 3
DsRole_RoleBackupDomainController = 4
DsRole_RolePrimaryDomainController = 5

class Machine(object):
    def __init__(self, monkey_guid):
        self.monkey_guid = str(monkey_guid)
    
    def GetHostName(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        names = set()

        for doc in cur:
            for comp in doc["data"]["Win32_ComputerSystem"]:
                names.add(eval(comp["Name"]))

        if len(names) == 1:
            return names.pop()

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

        SIDs = set()

        for doc in cur:
            for group_user in doc["data"]["Win32_GroupUser"]:
                if eval(group_user["GroupComponent"]["SID"]) != sid:
                    continue

                SIDs.add(eval(group_user["PartComponent"]["SID"]))
        
        return SIDs

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
        return self.GetUsersByGroupSid(self.GetGroupSidByGroupName("Administrators"))

    def GetDomainAdminsOfMachine(self):
        domain_name = self.GetDomainName()
        DCs = self.GetDomainControllersMonkeyGuidByDomainName(domain_name)
        
        domain_admins = set()
        
        for dc_monkey_guid in DCs:
            domain_admins += Machine(dc_monkey_guid).GetLocalAdmins()
        
        return domain_admins

    def GetAdmins(self):
        return self.GetLocalAdmins() | self.GetDomainAdminsOfMachine()
        
    def GetCachedSids(self):
        cur = db.telemetry.find({"telem_type":"system_info_collection", "monkey_guid": self.monkey_guid})
        
        SIDs = set()
        
        for doc in cur:
            for username in doc["data"]["credentials"]:
                SIDs.add(self.GetSidByUsername(username))
        
        return SIDs

def GetAllMachines():
    cur = db.telemetry.find({"telem_type":"system_info_collection"})
    
    GUIDs = set()
    
    for doc in cur:
        GUIDs.add(doc["monkey_guid"])

    return GUIDs

vertices = GetAllMachines()
edges = set()

for attacker in vertices:
    cached = Machine(attacker).GetCachedSids()

    for victim in vertices:
        if attacker == victim:
            continue

        admins = Machine(victim).GetAdmins()
        
        if len(cached & admins) > 0:
            edges.add((attacker, victim))

print vertices
print edges