"""Client for interacting with Object Storage. This is the top-level interface.

Note: this Client is a thin wrapper over the GCS Python Library. As a result,
many docstrings are borrowed from the underlying library.
"""

from typing import Optional

import requests
from google.auth import identity_pool
from google.cloud import storage
from replit.storage.config import REPLIT_ADC, REPLIT_DEFAULT_BUCKET_URL
from replit.storage.errors import DefaultBucketError


class Client:
  """Client manages interactions with Replit Object Storage.
    
  If multiple buckets are used within an application, one Client should be used
  per bucket.
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

  def delete(self, object_name: str) -> None:
    """Deletes an object from Object Storage.

    Args:
        object_name: The name of the object to be deleted.
    """
    return self.__object(object_name).delete()

  def download_as_bytes(self, object_name: str) -> bytes:
    """Download the contents an object as a bytes object.

    Args:
        object_name: The name of the object to be downloaded.
    """
    return self.__object(object_name).download_as_bytes()

  def download_as_string(self, object_name: str) -> str:
    """Download the contents an object as a string.

    Args:
        object_name: The name of the object to be downloaded.
    """
    return self.__object(object_name).download_as_text()

  def download_to_file(self, object_name: str, dest_file) -> None:
    """Download the contents an object into a file-like object.

    Args:
        object_name: The name of the object to be downloaded.
        dest_file: A file-like object.
    """
    return self.__object(object_name).download_to_file(dest_file)

  def download_to_filename(self, object_name: str, dest_filename: str) -> None:
    """Download the contents an object into a file on the local disk.

    Args:
        object_name: The name of the object to be downloaded.
        dest_filename: The filename of the file on the local disk to be written.
    """
    return self.__object(object_name).download_to_filename(dest_filename)

  def exists(self, object_name: str) -> bool:
    """Checks if an object exist.

    Args:
        object_name: The name of the object to be checked.
    """
    return self.__object(object_name).exists()

  def upload_from_file(self, dest_object_name: str, src_file) -> None:
    """Uploads the contents of a file-like object.

    Args:
        dest_object_name: The name of the object to be uploaded.
        src_file: A file-like object.
    """
    self.__object(dest_object_name).upload_from_file(src_file)

  def upload_from_filename(self, dest_object_name: str,
                           src_filename: str) -> None:
    """Upload an object from a file on the local disk.

    Args:
        dest_object_name: The name of the object to be uploaded.
        src_filename: The filename of a file on the local disk
    """
    self.__object(dest_object_name).upload_from_filename(src_filename)

  def upload_from_string(self, dest_object_name: str, src_data: str) -> None:
    """Upload an object from a string.

    Args:
        dest_object_name: The name of the object to be uploaded.
        src_data: The text to be uploaded.
    """
    self.__object(dest_object_name).upload_from_string(src_data)

  def __object(self, object_name: str) -> storage.Blob:
    if self.__gcs_bucket_handle is None:
      self.__gcs_bucket_handle = self.__get_bucket_handle()

    return self.__gcs_bucket_handle.blob(object_name)

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
