class RepositoryError(RuntimeError):
    """
    Raised when a repository encounters an error while attempting any operation.
    """


class RemovalError(RepositoryError):
    """
    Raised when a repository encounters an error while attempting to remove data.
    """


class RetrievalError(RepositoryError):
    """
    Raised when a repository encounters an error while attempting to retrieve data.
    """


class StorageError(RepositoryError):
    """
    Raised when a repository encounters an error while attempting to store data.
    """


class UnknownRecordError(RepositoryError):
    """
    Raised when the repository does not contain any data matching the request.
    """
