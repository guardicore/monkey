from unittest import TestCase
from unittest.mock import Mock

from infection_monkey.network.postgresql_fingerprint import PostgreSQLFinger

IRRELEVANT_EXCEPTION_STRING = "This is an irrelevant exception string."

RELEVANT_EXCEPTION_STRINGS =\
    {
        'pwd_auth_failed': 'FATAL:  password authentication failed for user "root"',
        'ssl_on_entry_not_found': 'FATAL:  no pg_hba.conf entry for host "127.0.0.1",'
                                  'user "random", database "postgres", SSL on',
        'ssl_off_entry_not_found': 'FATAL:  no pg_hba.conf entry for host "127.0.0.1",'
                                   'user "random", database "postgres", SSL off'
    }

RESULT_STRINGS =\
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

EXAMPLE_EXCEPTIONS_WITH_EXPECTED_RESULTS =\
    {
        # SSL not configured, all non-SSL allowed,  # SSL not configured, all non-SSL allowed
        RELEVANT_EXCEPTION_STRINGS['pwd_auth_failed']: [
            RESULT_STRINGS['ssl_not_conf'],
            RESULT_STRINGS['all_non_ssl']
        ],

        # SSL not configured, selected non-SSL allowed
        RELEVANT_EXCEPTION_STRINGS['ssl_off_entry_not_found']: [
            RESULT_STRINGS['ssl_not_conf'],
            RESULT_STRINGS['selected_non_ssl']
        ],

        # all SSL allowed, all non-SSL allowed
        '\n'.join([RELEVANT_EXCEPTION_STRINGS['pwd_auth_failed'],
                  RELEVANT_EXCEPTION_STRINGS['pwd_auth_failed']]): [
            RESULT_STRINGS['ssl_conf'],
            RESULT_STRINGS['all_ssl'],
            RESULT_STRINGS['all_non_ssl']
        ],

        # all SSL allowed, selected non-SSL allowed
        '\n'.join([RELEVANT_EXCEPTION_STRINGS['pwd_auth_failed'],
                  RELEVANT_EXCEPTION_STRINGS['ssl_off_entry_not_found']]): [
            RESULT_STRINGS['ssl_conf'],
            RESULT_STRINGS['all_ssl'],
            RESULT_STRINGS['selected_non_ssl']
        ],

        # selected SSL allowed, all non-SSL allowed
        '\n'.join([RELEVANT_EXCEPTION_STRINGS['ssl_on_entry_not_found'],
                  RELEVANT_EXCEPTION_STRINGS['pwd_auth_failed']]): [
            RESULT_STRINGS['ssl_conf'],
            RESULT_STRINGS['selected_ssl'],
            RESULT_STRINGS['all_non_ssl']
        ],

        # selected SSL allowed, selected non-SSL allowed
        '\n'.join([RELEVANT_EXCEPTION_STRINGS['ssl_on_entry_not_found'],
                  RELEVANT_EXCEPTION_STRINGS['ssl_off_entry_not_found']]): [
            RESULT_STRINGS['ssl_conf'],
            RESULT_STRINGS['only_selected']
        ]
    }

# EXPECTED_RESULTS =\
#     [
        # [RESULT_STRINGS['ssl_not_conf'],
        #  RESULT_STRINGS['all_non_ssl']],  # SSL not configured, all non-SSL allowed

        # [RESULT_STRINGS['ssl_not_conf'],
        #  RESULT_STRINGS['selected_non_ssl']],  # SSL not configured, selected non-SSL allowed

        # [RESULT_STRINGS['ssl_conf'],
        #  RESULT_STRINGS['all_ssl'],
        #  RESULT_STRINGS['all_non_ssl']],  # all SSL allowed, all non-SSL allowed

        # [RESULT_STRINGS['ssl_conf'],
        #  RESULT_STRINGS['all_ssl'],
        #  RESULT_STRINGS['selected_non_ssl']],  # all SSL allowed, selected non-SSL allowed

        # [RESULT_STRINGS['ssl_conf'],
        #  RESULT_STRINGS['selected_ssl'],
        #  RESULT_STRINGS['all_non_ssl']],  # selected SSL allowed, all non-SSL allowed

    #     [RESULT_STRINGS['ssl_conf'],
    #      RESULT_STRINGS['only_selected']]  # selected SSL allowed, selected non-SSL allowed
    # ]  # don't change order!


class TestPostgreSQLFinger(TestCase):
    def test_is_relevant_exception(self):
        assert PostgreSQLFinger().is_relevant_exception(IRRELEVANT_EXCEPTION_STRING) is False
        for exception_string in EXAMPLE_EXCEPTIONS_WITH_EXPECTED_RESULTS:
            assert PostgreSQLFinger().is_relevant_exception(exception_string) is True

    def test_analyze_operational_error(self):
        host = Mock(['services'])
        host.services = {}
        for exception_string in EXAMPLE_EXCEPTIONS_WITH_EXPECTED_RESULTS:
            with self.subTest(msg=f"Checking result for exception: {exception_string}"):
                PostgreSQLFinger().analyze_operational_error(host, exception_string)
                assert host.services['PostgreSQL']['communication_encryption_details'] ==\
                    ''.join(EXAMPLE_EXCEPTIONS_WITH_EXPECTED_RESULTS[exception_string])
