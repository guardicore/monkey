SHORT_REQUEST_TIMEOUT = 2.5  # Seconds. Use where we expect timeout and for small data transactions.
MEDIUM_REQUEST_TIMEOUT = 5  # Seconds. Use where we don't expect timeout.
LONG_REQUEST_TIMEOUT = 15  # Seconds. Use where we don't expect timeout and operate heavy data.
CONNECTION_TIMEOUT = 3  # Seconds. Use for TCP, SSH and other connections that shouldn't take long.
