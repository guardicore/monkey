from monkey_island.cc.database import mongo
from monkey_island.cc.services.groups_and_users_consts import (GROUPTYPE,
                                                               USERTYPE)

__author__ = 'maor.rayzin'


class WMIHandler(object):
    ADMINISTRATORS_GROUP_KNOWN_SID = '1-5-32-544'

    def __init__(self, monkey_id, wmi_info, user_secrets):

        self.monkey_id = monkey_id
        self.info_for_mongo = {}
        self.users_secrets = user_secrets
        if not wmi_info:
            self.users_info = ""
            self.groups_info = ""
            self.groups_and_users = ""
            self.services = ""
            self.products = ""
        else:
            self.users_info = wmi_info['Win32_UserAccount']
            self.groups_info = wmi_info['Win32_Group']
            self.groups_and_users = wmi_info['Win32_GroupUser']
            self.services = wmi_info['Win32_Service']
            self.products = wmi_info['Win32_Product']

    def process_and_handle_wmi_info(self):

        self.add_groups_to_collection()
        self.add_users_to_collection()
        self.create_group_user_connection()
        self.insert_info_to_mongo()
        if self.info_for_mongo:
            self.add_admin(self.info_for_mongo[self.ADMINISTRATORS_GROUP_KNOWN_SID], self.monkey_id)
        self.update_admins_retrospective()
        self.update_critical_services()

    def update_critical_services(self):
        critical_names = ("W3svc", "MSExchangeServiceHost", "dns", 'MSSQL$SQLEXPRES')
        mongo.db.monkey.update({'_id': self.monkey_id}, {'$set': {'critical_services': []}})

        services_names_list = [str(i['Name'])[2:-1] for i in self.services]
        products_names_list = [str(i['Name'])[2:-2] for i in self.products]

        for name in critical_names:
            if name in services_names_list or name in products_names_list:
                mongo.db.monkey.update({'_id': self.monkey_id}, {'$addToSet': {'critical_services': name}})

    def build_entity_document(self, entity_info, monkey_id=None):
        general_properties_dict = {
            'SID': str(entity_info['SID'])[4:-1],
            'name': str(entity_info['Name'])[2:-1],
            'machine_id': monkey_id,
            'member_of': [],
            'admin_on_machines': []
        }

        if monkey_id:
            general_properties_dict['domain_name'] = None
        else:
            general_properties_dict['domain_name'] = str(entity_info['Domain'])[2:-1]

        return general_properties_dict

    def add_users_to_collection(self):
        for user in self.users_info:
            if not user.get('LocalAccount'):
                base_entity = self.build_entity_document(user)
            else:
                base_entity = self.build_entity_document(user, self.monkey_id)
            base_entity['NTLM_secret'] = self.users_secrets.get(base_entity['name'], {}).get('ntlm_hash')
            base_entity['SAM_secret'] = self.users_secrets.get(base_entity['name'], {}).get('sam')
            base_entity['secret_location'] = []

            base_entity['type'] = USERTYPE
            self.info_for_mongo[base_entity.get('SID')] = base_entity

    def add_groups_to_collection(self):
        for group in self.groups_info:
            if not group.get('LocalAccount'):
                base_entity = self.build_entity_document(group)
            else:
                base_entity = self.build_entity_document(group, self.monkey_id)
            base_entity['entities_list'] = []
            base_entity['type'] = GROUPTYPE
            self.info_for_mongo[base_entity.get('SID')] = base_entity

    def create_group_user_connection(self):
        for group_user_couple in self.groups_and_users:
            group_part = group_user_couple['GroupComponent']
            child_part = group_user_couple['PartComponent']
            group_sid = str(group_part['SID'])[4:-1]
            groups_entities_list = self.info_for_mongo[group_sid]['entities_list']
            child_sid = ''

            if isinstance(child_part, str):
                child_part = str(child_part)
                name = None
                domain_name = None
                if "cimv2:Win32_UserAccount" in child_part:
                    # domain user
                    domain_name = child_part.split('cimv2:Win32_UserAccount.Domain="')[1].split('",Name="')[0]
                    name = child_part.split('cimv2:Win32_UserAccount.Domain="')[1].split('",Name="')[1][:-2]

                if "cimv2:Win32_Group" in child_part:
                    # domain group
                    domain_name = child_part.split('cimv2:Win32_Group.Domain="')[1].split('",Name="')[0]
                    name = child_part.split('cimv2:Win32_Group.Domain="')[1].split('",Name="')[1][:-2]

                for entity in self.info_for_mongo:
                    if self.info_for_mongo[entity]['name'] == name and \
                            self.info_for_mongo[entity]['domain'] == domain_name:
                        child_sid = self.info_for_mongo[entity]['SID']
            else:
                child_sid = str(child_part['SID'])[4:-1]

            if child_sid and child_sid not in groups_entities_list:
                groups_entities_list.append(child_sid)

            if child_sid:
                if child_sid in self.info_for_mongo:
                    self.info_for_mongo[child_sid]['member_of'].append(group_sid)

    def insert_info_to_mongo(self):
        for entity in list(self.info_for_mongo.values()):
            if entity['machine_id']:
                # Handling for local entities.
                mongo.db.groupsandusers.update({'SID': entity['SID'],
                                                'machine_id': entity['machine_id']}, entity, upsert=True)
            else:
                # Handlings for domain entities.
                if not mongo.db.groupsandusers.find_one({'SID': entity['SID']}):
                    mongo.db.groupsandusers.insert_one(entity)
                else:
                    # if entity is domain entity, add the monkey id of current machine to secrets_location.
                    # (found on this machine)
                    if entity.get('NTLM_secret'):
                        mongo.db.groupsandusers.update_one({'SID': entity['SID'], 'type': USERTYPE},
                                                           {'$addToSet': {'secret_location': self.monkey_id}})

    def update_admins_retrospective(self):
        for profile in self.info_for_mongo:
            groups_from_mongo = mongo.db.groupsandusers.find({
                'SID': {'$in': self.info_for_mongo[profile]['member_of']}},
                {'admin_on_machines': 1})

            for group in groups_from_mongo:
                if group['admin_on_machines']:
                    mongo.db.groupsandusers.update_one({'SID': self.info_for_mongo[profile]['SID']},
                                                       {'$addToSet': {'admin_on_machines': {
                                                           '$each': group['admin_on_machines']}}})

    def add_admin(self, group, machine_id):
        for sid in group['entities_list']:
            mongo.db.groupsandusers.update_one({'SID': sid},
                                               {'$addToSet': {'admin_on_machines': machine_id}})
            entity_details = mongo.db.groupsandusers.find_one({'SID': sid},
                                                              {'type': USERTYPE, 'entities_list': 1})
            if entity_details.get('type') == GROUPTYPE:
                self.add_admin(entity_details, machine_id)
