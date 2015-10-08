import subprocess
import sys
import platform

class FirewallApp(object):
    def is_enabled(self, **kwargs):
        return False

    def add_firewall_rule(self, **kwargs):
        return False

    def remove_firewall_rule(self, **kwargs):
        return False

    def listen_allowed(self, **kwargs):
        return True

    def __exit__(self):
        self.close()        

    def close(self):
        return

def _run_netsh_cmd(command, args):
    cmd = subprocess.Popen("netsh %s %s" % (command, " ".join(['%s="%s"'%(key,value) for key,value in args.items()])), stdout=subprocess.PIPE)
    return cmd.stdout.read().strip().lower().endswith('ok.')

class WinAdvFirewall(FirewallApp):
    def __init__(self):
        self._rules = {}

    def is_enabled(self):
        try:
            cmd = subprocess.Popen('netsh advfirewall show currentprofile', stdout=subprocess.PIPE)
            out = cmd.stdout.readlines()

            for l in out:
                if l.startswith('State'):
                    state = l.split()[-1].strip()

            return state == "ON"
        except:
            return None

    def add_firewall_rule(self, name="Firewall", dir="in", action="allow", program=sys.executable, **kwargs):
        netsh_args = {'name': name,
                      'dir' : dir,
                      'action': action,
                      'program' : program}
        netsh_args.update(kwargs)
        try:
            if _run_netsh_cmd('advfirewall firewall add rule', netsh_args):
                self._rules[name] = netsh_args
                return True
            else:
                return False
        except:
            return None

    def remove_firewall_rule(self, name="Firewall", **kwargs):
        netsh_args = {'name': name}
        netsh_args.update(kwargs)

        try:
            if _run_netsh_cmd('advfirewall firewall delete rule', netsh_args):
                if self._rules.has_key(name):
                    del self._rules[name]
                return True
            else:
                return False 
        except:
            return None

    def listen_allowed(self, **kwargs):
        if False == self.is_enabled():
            return True

        for rule in self._rules.values():
            if rule.get('program') == sys.executable and \
                'in' == rule.get('dir') and \
                'allow' == rule.get('action') and \
                4 == len(rule.keys()):
                return True
        return False

    def close(self):
        try:
            for rule in self._rules.keys():
                _run_netsh_cmd('advfirewall firewall delete rule', {'name' : rule})
        except:
            pass


class WinFirewall(FirewallApp):
    def __init__(self):
        self._rules = {}

    def is_enabled(self):
        try:
            cmd = subprocess.Popen('netsh firewall show state', stdout=subprocess.PIPE)
            out = cmd.stdout.readlines()

            for l in out:
                if l.startswith('Operational mode'):
                    state = l.split('=')[-1].strip()
                elif l.startswith('The service has not been started.'):
                    return False

            return state == "Enable"
        except:
            return None

    def add_firewall_rule(self, rule='allowedprogram', name="Firewall", mode="ENABLE", program=sys.executable, **kwargs):
        netsh_args = {'name': name,
                      'mode' : mode,
                      'program' : program}
        netsh_args.update(kwargs)

        try:
            if _run_netsh_cmd('firewall add', netsh_args):
                self._rules[name] = netsh_args
                return True
            else:
                return False 
        except:
            return None

    def remove_firewall_rule(self, rule='allowedprogram', name="Firewall", **kwargs):
        netsh_args = {'name': name,
                      'mode' : mode,
                      'program' : program}
        netsh_args.update(kwargs)
        try:
            if _run_netsh_cmd('firewall delete', netsh_args):
                if self._rules.has_key(name):
                    del self._rules[name]
                return True
            else:
                return False 
        except:
            return None

    def listen_allowed(self, **kwargs):
        if False == self.is_enabled():
            return True

        for rule in self._rules.values():
            if rule.get('program') == sys.executable and \
                'allowedprogram' == rule.get('rule') and \
                'ENABLE' == rule.get('mode') and \
                4 == len(rule.keys()):
                return True
        return False            

    def close(self):
        try:
            for rule in self._rules.keys():
                _run_netsh_cmd('firewall delete', {'name' : rule})
        except:
            pass

if sys.platform == "win32":
    try:
        win_ver = int(platform.version().split('.')[0])
    except:
        win_ver = 0
    if win_ver > 5:
        app = WinAdvFirewall()
    else:
        app = WinFirewall()
else:
    app = FirewallApp()