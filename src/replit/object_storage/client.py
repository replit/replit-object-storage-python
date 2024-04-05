"""Client for interacting with Object Storage. This is the top-level interface.

Note: this Client is a thin wrapper over the GCS Python Library. As a result,
many docstrings are borrowed from the underlying library.
"""

from typing import List, Optional, Union

import requests
from google.auth import identity_pool
from google.cloud import storage
from google.cloud.exceptions import NotFound

from replit.object_storage._config import REPLIT_ADC, REPLIT_DEFAULT_BUCKET_URL
from replit.object_storage.errors import (
  DefaultBucketError,
  ObjectNotFoundError,
  _google_error_handler,
)
from replit.object_storage.object import Object


class Client:
  """Client manages interactions with Replit Object Storage.
    
  If multiple buckets are used within an application, one Client should be used
  per bucket

  Any method may return one of the following errors:
  - `BucketNotFoundError`: If the bucket configured for the client could not be found.
  - `DefaultBucketError`: If no bucket was explicitly configured and an error occurred
      when resolving the default bucket.
  - `ForbiddenError`: If access to the requested resource is not allowed.
  - `TooManyRequestsError`: If rate limiting occurs.
  - `UnauthorizedError`: If the requested operation is not allowed.
  """

  __gcs_client: storage.Client

  __bucket_id: Optional[str] = None
  __gcs_bucket_handle: Optional[storage.Bucket] = None

  def __init__(self, bucket_id: Optional[str] = None):
    """Creates a new Client.

    Args:
        bucket_id: The ID of the bucket this Client should interface with.
            If no ID is defined, the Repl / Deployment's default bucket will be
            used.
    """
    creds = identity_pool.Credentials(**REPLIT_ADC)
    if bucket_id:
      self.__bucket_id = bucket_id
    self.__gcs_client = storage.Client(credentials=creds, project="")
    self.__gcs_bucket_handle = None

  @_google_error_handler
  def copy(self, object_name: str, dest_object_name: str) -> None:
    """Copies the specified object within the same bucket.

    If an object exists in the same location, it will be overwritten.

    Args:
        object_name: The full path of the object to be copied.
        dest_object_name: The full path to copy the object to.

    Raises:
        ObjectNotFoundError: If the source object could not be found.
    """
    source_object = self.__object(object_name)
    bucket = self.__bucket()
    bucket.copy_blob(
      source_object,
      bucket,
      dest_object_name,
    )

  @_google_error_handler
  def delete(self, object_name: str, ignore_not_found: bool = False) -> None:
    """Deletes an object from Object Storage.

    Args:
        object_name: The name of the object to be deleted.
        ignore_not_found: Whether an error should be raised if the object does not
          exist.

    Raises:
        ObjectNotFoundError: If the object could not be found.
    """
    try:
      return self.__object(object_name).delete()
    except NotFound as err:
      if ignore_not_found:
        return
      raise ObjectNotFoundError("The requested object could not be found.") from err

  @_google_error_handler
  def download_as_bytes(self, object_name: str) -> bytes:
    """Download the contents an object as a bytes object.

    Args:
        object_name: The name of the object to be downloaded.

    Returns:
        The raw byte representation of the object's contents.

    Raises:
        ObjectNotFoundError: If the object could not be found.
    """
    return self.__object(object_name).download_as_bytes()

  @_google_error_handler
  def download_as_text(self, object_name: str) -> str:
    """Download the contents an object as a string.

    Args:
        object_name: The name of the object to be downloaded.

    Returns:
        The object's contents as a UTF-8 encoded string.

    Raises:
        ObjectNotFoundError: If the object could not be found.
    """
    return self.__object(object_name).download_as_text()

  @_google_error_handler
  def download_to_filename(self, object_name: str, dest_filename: str) -> None:
    """Download the contents an object into a file on the local disk.

    Args:
        object_name: The name of the object to be downloaded.
        dest_filename: The filename of the file on the local disk to be written.

    Raises:
        ObjectNotFoundError: If the object could not be found.
    """
    return self.__object(object_name).download_to_filename(dest_filename)

  @_google_error_handler
  def exists(self, object_name: str) -> bool:
    """Checks if an object exist.

    Args:
        object_name: The name of the object to be checked.

    Returns:
        Whether or not the object exists.
    """
    return self.__object(object_name).exists()

  @_google_error_handler
  def list(
      self,
      end_offset: Optional[str] = None,
      match_glob: Optional[str] = None,
      max_results: Optional[int] = None,
      prefix: Optional[str] = None,
      start_offset: Optional[str] = None,
  ) -> List[Object]:
    """Lists objects in the bucket.

    Args:
        end_offset: Filter results to objects whose names are lexicographically
            before end_offset. If start_offset is also set, the objects listed
            have names between start_offset (inclusive) and end_offset
            (exclusive).
        match_glob: Glob pattern used to filter results, for example foo*bar.
        max_results: The maximum number of results that can be returned in the
            response.
        prefix: Filter results to objects who names have the specified prefix.
        start_offset: Filter results to objects whose names are
            lexicographically equal to or after start_offset. If endOffset is
            also set, the objects listed have names between start_offset
            (inclusive) and end_offset (exclusive).

    Returns:
        A list of objects matching the given query parameters. 
    """
    iter = self.__bucket().list_blobs(
        end_offset=end_offset,
        match_glob=match_glob,
        max_results=max_results,
        prefix=prefix,
        start_offset=start_offset,
    )
    return [Object(name=object.name) for object in iter]

  @_google_error_handler
  def upload_from_filename(self, dest_object_name: str,
                           src_filename: str) -> None:
    """Upload an object from a file on the local disk.

    Args:
        dest_object_name: The name of the object to be uploaded.
        src_filename: The filename of a file on the local disk
    """
    self.__object(dest_object_name).upload_from_filename(src_filename)

  @_google_error_handler
  def upload_from_bytes(self, dest_object_name: str, src_data: bytes) -> None:
    """Upload an object from bytes.

    Args:
        dest_object_name: The name of the object to be uploaded.
        src_data: The bytes to be uploaded.
    """
    self.__object(dest_object_name).upload_from_string(src_data)

  @_google_error_handler
  def upload_from_text(
    self,
    dest_object_name: str,
    src_data: Union[bytes, str]
  ) -> None:
    """Upload an object from a string.

    Args:
        dest_object_name: The name of the object to be uploaded.
        src_data: The text to be uploaded.
    """
    self.__object(dest_object_name).upload_from_string(src_data)

  def __bucket(self) -> storage.Bucket:
    if self.__gcs_bucket_handle is None:
      self.__gcs_bucket_handle = self.__get_bucket_handle()
    return self.__gcs_bucket_handle

  def __object(self, object_name: str) -> storage.Blob:
    return self.__bucket().blob(object_name)

  def __get_bucket_handle(self) -> storage.Bucket:
    if self.__bucket_id is None:
      self.__bucket_id = self.__get_default_bucket_id()
    return self.__gcs_client.bucket(self.__bucket_id)

  @staticmethod
  def __get_default_bucket_id() -> str:
    response = requests.get(REPLIT_DEFAULT_BUCKET_URL)
    try:
      response.raise_for_status()
    except requests.HTTPError as exc:
      raise DefaultBucketError("failed to request default bucket") from exc

    bucket_id = response.json().get("bucketId", "")
    if bucket_id == "":
      raise DefaultBucketError("no default bucket was specified, it may need "
                               "to be configured in .replit")

    return bucket_id
