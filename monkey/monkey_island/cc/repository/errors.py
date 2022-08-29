class RemovalError(RuntimeError):
    """
    Raised when a repository encounters an error while attempting to remove data.
    """


class RetrievalError(RuntimeError):
    """
    Raised when a repository encounters an error while attempting to retrieve data.
    """


class StorageError(RuntimeError):
    """
    Raised when a repository encounters an error while attempting to store data.
    """


class UnknownRecordError(RuntimeError):
    """
    Raised when the repository does not contain any data matching the request.
    """
