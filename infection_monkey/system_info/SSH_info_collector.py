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

    default_dirs = ['/.ssh/', '/']

    @staticmethod
    def get_info():
        LOG.info("Started scanning for ssh keys")
        home_dirs = SSHCollector.get_home_dirs()
        ssh_info = SSHCollector.get_ssh_files(home_dirs)
        LOG.info("Scanned for ssh keys")
        return ssh_info

    @staticmethod
    def get_ssh_struct(name, home_dir):
        """
        :return: SSH info struct with these fields:
        name: username of user, for whom the keys belong
        home_dir: users home directory
        public_key: contents of *.pub file(public key)
        private_key: contents of * file(private key)
        known_hosts: contents of known_hosts file(all the servers keys are good for,
        possibly hashed)
        """
        return {'name': name, 'home_dir': home_dir, 'public_key': None,
                      'private_key': None, 'known_hosts': None}

    @staticmethod
    def get_home_dirs():
        root_dir = SSHCollector.get_ssh_struct('root', '/')
        home_dirs = [SSHCollector.get_ssh_struct(x.pw_name,x.pw_dir) for x in pwd.getpwall()
                      if x.pw_dir.startswith('/home')]
        home_dirs.append(root_dir)
        return home_dirs

    @staticmethod
    def get_ssh_files(usr_info):
        for info in usr_info:
            path = info['home_dir']
            for directory in SSHCollector.default_dirs:
                if os.path.isdir(path + directory):
                    try:
                        current_path = path + directory
                        # searching for public key
                        if glob.glob(current_path+'*.pub'):
                            public = (glob.glob(current_path+'*.pub')[0])
                            LOG.info("Found public key in %s" % public)
                            try:
                                with open(public) as f:
                                    info['public_key'] = f.read()
                                private = public.rsplit('.', 1)[0]
                                if os.path.exists(private):
                                    try:
                                        with open(private) as f:
                                            info['private_key'] = f.read()
                                            LOG.info("Found private key in %s" % private)
                                    except (IOError, OSError):
                                        pass
                                if os.path.exists(current_path + '/known_hosts'):
                                    try:
                                        with open(current_path + '/known_hosts') as f:
                                            info['known_hosts'] = f.read()
                                            LOG.info("Found known_hosts in %s" % current_path+'/known_hosts')
                                    except (IOError, OSError):
                                        pass
                            except (IOError, OSError):
                                pass
                    except OSError:
                        pass
        usr_info = [info for info in usr_info if info['private_key'] or info['known_hosts']
                    or info['public_key']]
        return usr_info
