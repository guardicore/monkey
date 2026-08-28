import json
import logging
import platform
import subprocess
import sys

from common.common_consts.timeouts import SHORT_REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


def _run_powershell_json(ps_command):
    """
    Runs a PowerShell command that outputs JSON and parses it.
    Locale-independent: PowerShell object property names (Enabled, Name, etc.)
    never change based on the system's display language, unlike netsh's
    human-readable text output.
    """
    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_command],
        capture_output=True,
        timeout=SHORT_REQUEST_TIMEOUT,
    )
    output = result.stdout.decode("utf-8", errors="ignore").strip()
    if not output:
        return None
    data = json.loads(output)
    if isinstance(data, dict):
        data = [data]
    return data


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
    """
    Manages the Windows Firewall (Vista/Server 2008 and later) via PowerShell's
    NetSecurity module instead of parsing netsh's localized text output.
    """

    def __init__(self):
        self._rules = {}

    def is_enabled(self):
        try:
            profiles = _run_powershell_json(
                "Get-NetFirewallProfile | Select-Object Enabled | ConvertTo-Json -Compress"
            )
            if not profiles:
                return None
            return any(bool(p.get("Enabled")) for p in profiles)
        except subprocess.TimeoutExpired:
            return None
        except Exception:
            return None

    def add_firewall_rule(
        self, name="MonkeyRule", direction="in", action="allow", program=sys.executable, **kwargs
    ):
        direction_ps = "Inbound" if direction.lower().startswith("in") else "Outbound"
        action_ps = "Allow" if action.lower().startswith("allow") else "Block"
        ps_command = (
            'New-NetFirewallRule -DisplayName "{name}" -Direction {direction} '
            '-Action {action} -Program "{program}" -Confirm:$false | Out-Null; '
            "if ($?) {{ Write-Output '[{{\"Success\":true}}]' }} "
            "else {{ Write-Output '[{{\"Success\":false}}]' }}"
        ).format(name=name, direction=direction_ps, action=action_ps, program=program)

        try:
            result = _run_powershell_json(ps_command)
            success = bool(result) and result[0].get("Success") is True
            if success:
                netsh_args = {"name": name, "dir": direction, "action": action, "program": program}
                netsh_args.update(kwargs)
                self._rules[name] = netsh_args
            return success
        except subprocess.TimeoutExpired:
            logger.info("Timeout expired trying to add a firewall rule.")
            return None
        except Exception as err:
            logger.info(f"Failed adding a firewall rule: {err}")
            return None

    def remove_firewall_rule(self, name="Firewall", **kwargs):
        ps_command = (
            'Remove-NetFirewallRule -DisplayName "{name}" -Confirm:$false | Out-Null; '
            "if ($?) {{ Write-Output '[{{\"Success\":true}}]' }} "
            "else {{ Write-Output '[{{\"Success\":false}}]' }}"
        ).format(name=name)

        try:
            result = _run_powershell_json(ps_command)
            success = bool(result) and result[0].get("Success") is True
            if success and name in self._rules:
                del self._rules[name]
            return success
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
    """
    Legacy pre-Vista/Server 2008 Windows Firewall (netsh firewall, not
    advfirewall). Only reachable on Windows XP/Server 2003, which are long out
    of support -- kept as a safety-patched fallback, not modernized.
    """

    def __init__(self):
        self._rules = {}

    def is_enabled(self):
        try:
            cmd = subprocess.Popen("netsh firewall show state", stdout=subprocess.PIPE)
            out = cmd.stdout.readlines()
            state = None

            for raw_line in out:
                line = raw_line.decode(errors="ignore")
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
            output = subprocess.check_output(
                "netsh firewall add %s %s"
                % (
                    rule,
                    " ".join(
                        ['%s="%s"' % (k, v) for k, v in list(netsh_args.items()) if v]
                    ),
                ),
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            if output.strip().lower().endswith(b"ok."):
                netsh_args["rule"] = rule
                self._rules[name] = netsh_args
                return True
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
            output = subprocess.check_output(
                "netsh firewall delete %s %s"
                % (
                    rule,
                    " ".join(
                        ['%s="%s"' % (k, v) for k, v in list(netsh_args.items()) if v]
                    ),
                ),
                timeout=SHORT_REQUEST_TIMEOUT,
            )
            if output.strip().lower().endswith(b"ok."):
                if name in self._rules:
                    del self._rules[name]
                return True
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