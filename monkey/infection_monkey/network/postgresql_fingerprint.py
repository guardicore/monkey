"""
Implementation from https://github.com/SecuraBV/CVE-2020-1472
"""

import logging

import psycopg2

from infection_monkey.network.HostFinger import HostFinger

LOG = logging.getLogger(__name__)


class PostgreSQLFinger(HostFinger):
    """
    Fingerprints PostgreSQL databases, only on port 5432
    """
    # Class related consts
    _SCANNED_SERVICE = 'PostgreSQL'
    POSTGRESQL_DEFAULT_PORT = 5432
    CREDS = {'username': 'monkeySaysHello',
             'password': 'monkeySaysXXX'}

    def get_host_fingerprint(self, host):
        try:
            connection = psycopg2.connect(host=host.ip_addr,
                                          port=self.POSTGRESQL_DEFAULT_PORT,
                                          user=self.CREDS['username'],
                                          password=self.CREDS['password'],
                                          sslmode='prefer')  # don't need to worry about DB name; creds are wrong, won't check

        except psycopg2.OperationalError as ex:
            # try block will throw an OperationalError since the credentials are wrong, which we then analyze
            self.relevant_ex_substrings = ["password authentication failed",
                                           "entry for host"]  # "no pg_hba.conf entry for host" but filename may be diff
            exception_string = str(ex)

            if not any(substr in exception_string for substr in self.relevant_ex_substrings):
                # OperationalError due to some other reason
                return False

            self.init_service(host.services, self._SCANNED_SERVICE, self.POSTGRESQL_DEFAULT_PORT)

            ssl_connection_details = []
            exceptions = exception_string.split("\n")
            ssl_conf_on_server = self.is_ssl_configured(exceptions)

            """ Make this part cleaner and better! """

            # SSL configured
            if ssl_conf_on_server:
                ssl_connection_details.append("SSL is configured on the PostgreSQL server.\n")
                # SSL
                if self.found_entry_for_host_but_pwd_auth_failed(exceptions[0]):
                    ssl_connection_details.append("SSL connections can be made by all.\n")
                else:
                    ssl_connection_details.append(
                        "SSL connections can be made by selected hosts only OR non-SSL usage is forced.\n")
                # non-SSL
                if self.found_entry_for_host_but_pwd_auth_failed(exceptions[1]):
                    ssl_connection_details.append("Non-SSL connections can be made by all.\n")
                else:
                    ssl_connection_details.append(
                        "Non-SSL connections can be made by selected hosts only OR SSL usage is forced.\n")

            # SSL not configured
            else:
                ssl_connection_details.append("SSL is NOT configured on the PostgreSQL server.\n")
                if self.found_entry_for_host_but_pwd_auth_failed(exceptions[0]):
                    ssl_connection_details.append("Non-SSL connections can be made by all.\n")
                else:
                    ssl_connection_details.append(
                        "Non-SSL connections can be made by selected hosts only OR SSL usage is forced.\n")

            host.services[self._SCANNED_SERVICE]['communication_encryption_details'] = ''.join(ssl_connection_details)

            return True

    def is_ssl_configured(self, exceptions):
        # when trying to authenticate, it checks pg_hba.conf file:
        # first, for a record where it can connect with SSL and second, without SSL
        if len(exceptions) == 1:  # SSL not configured on server so only checks for non-SSL record
            return False
        elif len(exceptions) == 2:  # SSL configured so checks for both
            return True

    def found_entry_for_host_but_pwd_auth_failed(self, exception):
        if self.relevant_ex_substrings[0] in exception:
            return True  # entry found in pg_hba.conf file but password authentication failed
        return False  # entry not found in pg_hba.conf file
