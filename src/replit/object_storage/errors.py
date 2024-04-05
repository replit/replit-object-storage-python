"""Errors that may be returned by the storage library."""
from functools import wraps

from google.cloud.exceptions import (
  Forbidden,
  NotFound,
  TooManyRequests,
  Unauthorized,
)


class BucketNotFoundError(Exception):
  """BucketNotFoundError may occur if the specified bucket could not be found."""
  pass


class DefaultBucketError(Exception):
  """DefaultBucketError may occur if the default bucket could not be resolved."""
  pass


class ForbiddenError(Exception):
  """ForbiddenError may occur if access to the requested resource is not allowed."""
  pass


class ObjectNotFoundError(Exception):
  """ObjectNotFoundError may occur if the requested object could not be found."""
  pass


class TooManyRequestsError(Exception):
    """TooManyRequestsError may occur if the rate of requests exceeds the rate limit."""
    pass


class UnauthorizedError(Exception):
  """UnauthorizedError may occur if the requested operation is not allowed."""
  pass


def _google_error_handler(func):
  """Wraps functions that call GCP APIs and handles common errors.

  Common errors are re-raised in more digestable formats, less common errors are passed
  through.
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Forbidden as err:
      raise ForbiddenError("Access to the requested resource is not allowed.") from err
    except NotFound as err:
      if "The specified bucket does not exist." in err.message:
        raise BucketNotFoundError("The requested bucket could not be found.") from err
      raise ObjectNotFoundError(
          "The requested object could not be found.") from err
    except TooManyRequests as err:
      raise TooManyRequestsError("Rate limit exceeded.") from err
    except Unauthorized as err:
      raise UnauthorizedError("The requested operation is not allowed.") from err
    # Other exceptions we'll bubble up for now

  return wrapper
