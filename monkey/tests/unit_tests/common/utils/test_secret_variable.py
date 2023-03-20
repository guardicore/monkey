import logging

from common.utils.secret_variable import SecretVariable

SECRET_TEXT = "my_secret_value"


def test_secret_variable__no_logging(capsys):
    # Arrange
    secret_variable = SecretVariable(SECRET_TEXT)
    logger = logging.getLogger(__name__)
    # Act
    logger.debug(secret_variable)

    # Asser
    captured = capsys.readouterr()
    assert SECRET_TEXT not in captured.out
