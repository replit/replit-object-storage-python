from unittest.mock import MagicMock, patch

import pytest
import requests
from google.cloud import storage
from replit.object_storage import Client, DefaultBucketError

from tests.unit.replit.object_storage.mocks import (
    build_mock_default_bucket_response,
    build_mock_gcs_client,
)


@pytest.fixture(autouse=True)
def gcs_client():
  with patch.object(storage, "Client", build_mock_gcs_client()):
    yield


@pytest.fixture(autouse=True)
def requests_get():
  with patch.object(requests,
                    "get",
                    return_value=build_mock_default_bucket_response()):
    yield


def test_get_default_bucket_success():
  result = Client().exists("object-name")
  assert result


@patch.object(requests, "get")
def test_get_default_bucket_http_eror(mock_get):
  mock_response = MagicMock()
  mock_response.raise_for_status.side_effect = requests.HTTPError
  mock_get.return_value = mock_response

  with pytest.raises(DefaultBucketError):
    Client().exists("object-name")


@patch.object(requests, "get")
def test_get_default_bucket_malformed_response(mock_get):
  mock_response = MagicMock()
  mock_response.json.return_value = {}
  mock_get.return_value = mock_response

  with pytest.raises(DefaultBucketError):
    Client().exists("object-name")


def test_copy():
  result = Client("bucket-id").copy("object-name", "dest-object-name")
  assert result is None


def test_delete():
  result = Client("bucket-id").delete("object-name")
  assert result is None


def test_download_as_bytes():
  result = Client("bucket-id").download_as_bytes("object-name")
  assert result == str.encode("test-bytes")


def test_download_as_string():
  result = Client("bucket-id").download_as_string("object-name")
  assert result == "test-text"


def test_download_to_filename():
  result = Client("bucket-id").download_to_filename("object-name",
                                                    "dest-filename")
  assert result is None


def test_exists():
  result = Client("bucket-id").exists("object-name")
  assert isinstance(result, bool)
  assert result


def test_list():
  result = Client("bucket-id").list("object-name")
  assert isinstance(result, list)


def test_upload_from_filename():
  result = Client("bucket-id").upload_from_filename("object-name",
                                                    "src-filename")
  assert result is None


def test_upload_from_string():
  result = Client("bucket-id").upload_from_string("object-name", "src-text")
  assert result is None
