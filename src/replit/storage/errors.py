"""Errors that may be returned by the storage library."""


class DefaultBucketError(Exception):
    """DefaultBucketError may occur if the default bucket could not be resolved."""
    pass
