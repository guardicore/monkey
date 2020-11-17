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

        except psycopg2.OperationalError as ex:  # try block will throw an OperationalError since the credentials are wrong
            exception_string = str(ex)
            relevant_ex_substrings = ["password authentication failed",
                                      "entry for host"]  # "no pg_hba.conf entry for host" but filename may be diff

            if not any(substr in exception_string for substr in relevant_ex_substrings):
                # OperationalError due to some other reason
                return False

            self.init_service(host.services, self._SCANNED_SERVICE, self.POSTGRESQL_DEFAULT_PORT)

            """
                ---> split exception_string by \n

                if len == 1: ssl_conf_on_server = False
                    if "password authentication failed" is present: ssl_forced = False
                    elif "entry for host" is present: ssl_forced = True
                if len == 2: ssl_conf_on_server = True
                    // for [0]
                    if "password authentication failed" is present: ssl_all = True
                    elif "entry for host" is present: ssl_forced = False
                    // for [1]
                    if "password authentication failed" is present: nossl_all = True
                    elif "entry for host" is present: nossl_forced = False

                ---> def is_ssl_configured():
                        // check length after splitting
                ---> def is_ssl_exists():
                        if is_ssl_configured(): // checks twice - once for SSL entry, once for no SSL entry
                            koi_function() for [0]th // kisi function mein if-elif waala daal do upar jo likha hai
                        koi_function() for [-1]th

                // how do i make deriving the results simpler and shorter?!
            """

            # LOG.info(f'Exception: {ex}')
