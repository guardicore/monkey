
__author__ = 'maor.rayzin'


class MimikatzSecrets(object):

    def __init__(self):
        # Static class
        pass

    @staticmethod
    def extract_sam_secrets(mim_string, users_dict):
        users_secrets = mim_string.split("\n42.")[1].split("\nSAMKey :")[1].split("\n\n")[1:]

        if mim_string.count("\n42.") != 2:
            return {}

        for sam_user_txt in users_secrets:
            sam_user = dict([map(unicode.strip, line.split(":")) for line in
                             filter(lambda l: l.count(":") == 1, sam_user_txt.splitlines())])
            username = sam_user.get("User")
            users_dict[username] = {}

            ntlm = sam_user.get("NTLM")
            if "[hashed secret]" not in ntlm:
                continue

            users_dict[username]['SAM'] = ntlm.replace("[hashed secret]", "").strip()

    @staticmethod
    def extract_ntlm_secrets(mim_string, users_dict):

        if mim_string.count("\n42.") != 2:
            return {}

        ntds_users = mim_string.split("\n42.")[2].split("\nRID  :")[1:]

        for ntds_user_txt in ntds_users:
            user = ntds_user_txt.split("User :")[1].splitlines()[0].replace("User :", "").strip()
            ntlm = ntds_user_txt.split("* Primary\n    NTLM :")[1].splitlines()[0].replace("NTLM :", "").strip()
            ntlm = ntlm.replace("[hashed secret]", "").strip()
            users_dict[user] = {}
            if ntlm:
                users_dict[user]['ntlm'] = ntlm

    @staticmethod
    def extract_secrets_from_mimikatz(mim_string):
        users_dict = {}
        MimikatzSecrets.extract_sam_secrets(mim_string, users_dict)
        MimikatzSecrets.extract_ntlm_secrets(mim_string, users_dict)

        return users_dict
