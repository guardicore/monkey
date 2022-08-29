class RemovalError(RuntimeError):
    """
    Raised when a repository encounters an error while attempting to remove data.
    """

    pass


class RetrievalError(RuntimeError):
    """
    Raised when a repository encounters an error while attempting to retrieve data.
    """

    pass


class StorageError(RuntimeError):
    """
    Raised when a repository encounters an error while attempting to store data.
    """

    pass


class UnknownRecordError(RuntimeError):
    """
    Raised when the repository does not contain any data matching the request.
    """
