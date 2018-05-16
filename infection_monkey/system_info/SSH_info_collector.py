import logging
import pwd
import sys
import os
import glob

__author__ = 'VakarisZ'

LOG = logging.getLogger(__name__)


class SSHCollector(object):
    """
    SSH keys and known hosts collection module
    """

    default_dirs = ['/.ssh', '/']

    @staticmethod
    def get_info():
        home_dirs = SSHCollector.get_home_dirs()
        ssh_info = SSHCollector.get_ssh_files(home_dirs)
        LOG.info("Scanned for ssh keys")
        return ssh_info

    @staticmethod
    def get_home_dirs():
        home_dirs = [{'name': 'root', 'home_dir': '/root', 'public_key': None,
                      'private_key': None, 'known_hosts': None}]
        for usr in pwd.getpwall():
            if usr[5].startswith('/home'):
                ssh_data = {'name': usr[0], 'home_dir': usr[5], 'public_key': None,
                            'private_key': None, 'known_hosts': None}
                home_dirs.append(ssh_data)
        return home_dirs

    @staticmethod
    def get_ssh_files(usr_info):
        for info in usr_info:
            path = info['home_dir']
            for directory in SSHCollector.default_dirs:
                if os.path.isdir(path + directory):
                    try:
                        os.chdir(path + directory)
                        # searching for public key
                        if glob.glob('*.pub'):
                            public = '/' + (glob.glob('*.pub')[0])
                            try:
                                with open(path + directory + public) as f:
                                    info['public_key'] = f.read()
                                private = public.split('.')[0]
                            except:
                                pass
                            if os.path.exists(path + directory + private):
                                try:
                                    with open(path + directory + private) as f:
                                        info['private_key'] = f.read()
                                except:
                                    pass
                            if os.path.exists(path + directory + '/known_hosts'):
                                try:
                                    with open(path + directory + '/known_hosts') as f:
                                        info['known_hosts'] = f.read()
                                except:
                                    pass
                    except:
                        pass
        return usr_info
