import logging
import platform
import subprocess
import sys

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


def _run_netsh_cmd(command, args):
    output = subprocess.check_output(
        "netsh %s %s"
        % (
            command,
            " ".join(['%s="%s"' % (key, value) for key, value in list(args.items()) if value]),
        ),
        timeout=SHORT_REQUEST_TIMEOUT,
    )
    return output.strip().lower().endswith(b"ok.")


class FirewallApp(object):
    def is_enabled(self, **kwargs):
        return False

    def add_firewall_rule(self, **kwargs):
        return False

    def remove_firewall_rule(self, **kwargs):
        return False

    def listen_allowed(self, **kwargs):
        return True

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, value, traceback):
        self.close()

    def close(self):
        return


class WinAdvFirewall(FirewallApp):
    def __init__(self):
        self._rules = {}

    def is_enabled(self):
        try:
            out = subprocess.check_output(
                "netsh advfirewall show currentprofile", timeout=SHORT_REQUEST_TIMEOUT
            )
        except subprocess.TimeoutExpired:
            return None
        except Exception:
            return None

        for line in out.decode().splitlines():
            if line.startswith("State"):
                state = line.split()[-1].strip()
                return state == "ON"

        return None

    def add_firewall_rule(
        self, name="MonkeyRule", direction="in", action="allow", program=sys.executable, **kwargs
    ):
        netsh_args = {"name": name, "dir": direction, "action": action, "program": program}
        netsh_args.update(kwargs)
        try:
            if _run_netsh_cmd("advfirewall firewall add rule", netsh_args):
                self._rules[name] = netsh_args
                return True
            else:
                return False
        except subprocess.CalledProcessError as err:
            logger.info(f"Failed adding a firewall rule: {err.stdout}")
        except subprocess.TimeoutExpired:
            logger.info("Timeout expired trying to add a firewall rule.")
        return None

    def remove_firewall_rule(self, name="Firewall", **kwargs):
        netsh_args = {"name": name}
        netsh_args.update(kwargs)

        try:
            if _run_netsh_cmd("advfirewall firewall delete rule", netsh_args):
                if name in self._rules:
                    del self._rules[name]
                return True
            else:
                return False
        except Exception:
            return None

    def listen_allowed(self, **kwargs):
        if not self.is_enabled():
            return True

        for rule in list(self._rules.values()):
            if (
                rule.get("program") == sys.executable
                and "in" == rule.get("dir")
                and "allow" == rule.get("action")
                and 4 == len(list(rule.keys()))
            ):
                return True
        return False

    def close(self):
        try:
            for rule in list(self._rules.keys()):
                self.remove_firewall_rule(name=rule)
        except Exception:
            pass


class WinFirewall(FirewallApp):
    def __init__(self):
        self._rules = {}

    def is_enabled(self):
        try:
            cmd = subprocess.Popen("netsh firewall show state", stdout=subprocess.PIPE)
            out = cmd.stdout.readlines()

            for line in out:
                if line.startswith("Operational mode"):
                    state = line.split("=")[-1].strip()
                elif line.startswith("The service has not been started."):
                    return False

            return state == "Enable"
        except Exception:
            return None

    def add_firewall_rule(
        self,
        rule="allowedprogram",
        name="Firewall",
        mode="ENABLE",
        program=sys.executable,
        **kwargs,
    ):
        netsh_args = {"name": name, "mode": mode, "program": program}
        netsh_args.update(kwargs)

        try:
            if _run_netsh_cmd("firewall add %s" % rule, netsh_args):
                netsh_args["rule"] = rule
                self._rules[name] = netsh_args
                return True
            else:
                return False
        except Exception:
            return None

    def remove_firewall_rule(
        self,
        rule="allowedprogram",
        name="Firewall",
        mode="ENABLE",
        program=sys.executable,
        **kwargs,
    ):
        netsh_args = {"program": program}
        netsh_args.update(kwargs)
        try:
            if _run_netsh_cmd("firewall delete %s" % rule, netsh_args):
                if name in self._rules:
                    del self._rules[name]
                return True
            else:
                return False
        except Exception:
            return None

    def listen_allowed(self, **kwargs):
        if not self.is_enabled():
            return True

        for rule in list(self._rules.values()):
            if rule.get("program") == sys.executable and "ENABLE" == rule.get("mode"):
                return True
        return False

    def close(self):
        try:
            for rule in list(self._rules.values()):
                self.remove_firewall_rule(**rule)
        except Exception:
            pass


if sys.platform == "win32":
    try:
        win_ver = int(platform.version().split(".")[0])
    except Exception:
        win_ver = 0
    if win_ver > 5:
        app = WinAdvFirewall()
    else:
        app = WinFirewall()
else:
    app = FirewallApp()
