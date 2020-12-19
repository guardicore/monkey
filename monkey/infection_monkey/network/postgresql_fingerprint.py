import logging

import psycopg2

from infection_monkey.model import ID_STRING
from infection_monkey.network.HostFinger import HostFinger

LOG = logging.getLogger(__name__)


class PostgreSQLFinger(HostFinger):
    """
    Fingerprints PostgreSQL databases, only on port 5432
    """
    # Class related consts
    _SCANNED_SERVICE = 'PostgreSQL'
    POSTGRESQL_DEFAULT_PORT = 5432
    CREDS = {'username': ID_STRING,
             'password': ID_STRING}
    CONNECTION_DETAILS =\
        {
            'ssl_conf': "SSL is configured on the PostgreSQL server.\n",
            'ssl_not_conf': "SSL is NOT configured on the PostgreSQL server.\n",
            'all_ssl': "SSL connections can be made by all.\n",
            'all_non_ssl': "Non-SSL connections can be made by all.\n",
            'selected_ssl': "SSL connections can be made by selected hosts only OR "
                            "non-SSL usage is forced.\n",
            'selected_non_ssl': "Non-SSL connections can be made by selected hosts only OR "
                                "SSL usage is forced.\n",
            'only_selected': "Only selected hosts can make connections (SSL or non-SSL).\n"
        }
    RELEVANT_EX_SUBSTRINGS = ["password authentication failed",
                              "entry for host"]  # "no pg_hba.conf entry for host" but filename may be diff

    def get_host_fingerprint(self, host):
        try:
            psycopg2.connect(host=host.ip_addr,
                             port=self.POSTGRESQL_DEFAULT_PORT,
                             user=self.CREDS['username'],
                             password=self.CREDS['password'],
                             sslmode='prefer')  # don't need to worry about DB name; creds are wrong, won't check

        except psycopg2.OperationalError as ex:
            # try block will throw an OperationalError since the credentials are wrong, which we then analyze
            try:
                exception_string = str(ex)

                if not self.is_relevant_exception(exception_string):
                    return False

                # all's well; start analyzing errors
                self.analyze_operational_error(host, exception_string)
                return True

            except Exception as err:
                LOG.debug("Error getting PostgreSQL fingerprint: %s", err)

            return False

    def is_relevant_exception(self, exception_string):
        if not any(substr in exception_string for substr in self.RELEVANT_EX_SUBSTRINGS):
            # OperationalError due to some other reason - irrelevant exception
            return False
        return True

    def analyze_operational_error(self, host, exception_string):
        self.init_service(host.services, self._SCANNED_SERVICE, self.POSTGRESQL_DEFAULT_PORT)

        exceptions = exception_string.split("\n")

        ssl_connection_details = []
        ssl_conf_on_server = self.is_ssl_configured(exceptions)

        # SSL configured
        if ssl_conf_on_server:
            ssl_connection_details.append(self.CONNECTION_DETAILS['ssl_conf'])
            # SSL
            ssl_selected_comms_only = False
            if self.found_entry_for_host_but_pwd_auth_failed(exceptions[0]):
                ssl_connection_details.append(self.CONNECTION_DETAILS['all_ssl'])
            else:
                ssl_connection_details.append(self.CONNECTION_DETAILS['selected_ssl'])
                ssl_selected_comms_only = True
            # non-SSL
            if self.found_entry_for_host_but_pwd_auth_failed(exceptions[1]):
                ssl_connection_details.append(self.CONNECTION_DETAILS['all_non_ssl'])
            else:
                if ssl_selected_comms_only:  # if only selected SSL allowed and only selected non-SSL allowed
                    ssl_connection_details[-1] = self.CONNECTION_DETAILS['only_selected']
                else:
                    ssl_connection_details.append(self.CONNECTION_DETAILS['selected_non_ssl'])

        # SSL not configured
        else:
            ssl_connection_details.append(self.CONNECTION_DETAILS['ssl_not_conf'])
            if self.found_entry_for_host_but_pwd_auth_failed(exceptions[0]):
                ssl_connection_details.append(self.CONNECTION_DETAILS['all_non_ssl'])
            else:
                ssl_connection_details.append(self.CONNECTION_DETAILS['selected_non_ssl'])

        host.services[self._SCANNED_SERVICE]['communication_encryption_details'] = ''.join(ssl_connection_details)

    @staticmethod
    def is_ssl_configured(exceptions):
        # when trying to authenticate, it checks pg_hba.conf file:
        # first, for a record where it can connect with SSL and second, without SSL
        if len(exceptions) == 1:  # SSL not configured on server so only checks for non-SSL record
            return False
        elif len(exceptions) == 2:  # SSL configured so checks for both
            return True

    def found_entry_for_host_but_pwd_auth_failed(self, exception):
        if self.RELEVANT_EX_SUBSTRINGS[0] in exception:
            return True  # entry found in pg_hba.conf file but password authentication failed
        return False  # entry not found in pg_hba.conf file
