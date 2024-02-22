from unittest.mock import MagicMock


def build_mock_default_bucket_response() -> MagicMock:
    mock_response = MagicMock()
    mock_response.json.return_value = {"bucketId": "bucket-id"}
    return mock_response


def build_mock_gcs_client() -> MagicMock:
    mock_blob_handle = MagicMock()
    mock_blob_handle.delete.return_value = None
    mock_blob_handle.download_as_bytes.return_value = str.encode("test-bytes")
    mock_blob_handle.download_as_text.return_value = "test-text"
    mock_blob_handle.download_to_file.return_value = None
    mock_blob_handle.download_to_filename.return_value = None
    mock_blob_handle.exists.return_value = True
    mock_blob_handle.upload_from_file.return_value = None
    mock_blob_handle.upload_from_filename.return_value = None
    mock_blob_handle.upload_from_text.return_value = None

    mock_bucket_handle = MagicMock()
    mock_bucket_handle.blob.return_value = mock_blob_handle

    mock_gcs_client = MagicMock()
    mock_gcs_client.bucket.return_value = mock_bucket_handle

    mock_gcs_client_constructor = MagicMock(return_value=mock_gcs_client)
    return mock_gcs_client_constructor
