from tempfile import TemporaryDirectory
from uuid import uuid4

import pytest
from replit.object_storage import Client, Object
from replit.object_storage.errors import ObjectNotFoundError

TEST_FILE_CONTENTS = "Hello World!"


@pytest.fixture(scope='session', autouse=True)
def testdir():
  dir = str(uuid4())
  yield dir
  client = Client()
  for object in client.list(prefix=dir):
    client.delete(object.name)


class TestCopy:

  @staticmethod
  def test_upload_then_copy(testdir):
    client = Client()
    client.upload_from_text(f"{testdir}/copy-1-1.txt", TEST_FILE_CONTENTS)

    client.copy(f"{testdir}/copy-1-1.txt", f"{testdir}/copy-1-2.txt")
    exists = client.exists(f"{testdir}/copy-1-2.txt")
    assert exists


  @staticmethod
  def test_not_found(testdir):
    client = Client()
    with pytest.raises(ObjectNotFoundError):
      client.copy(f"{testdir}/copy-2-1.txt", f"{testdir}/copy-2-2.txt")


class TestDelete:

  @staticmethod
  def test_upload_then_delete(testdir):
    client = Client()
    client.upload_from_text(f"{testdir}/delete-1.txt", TEST_FILE_CONTENTS)
    exists = client.exists(f"{testdir}/delete-1.txt")
    assert exists

    client.delete(f"{testdir}/delete-1.txt")
    exists = client.exists(f"{testdir}/delete-1.txt")
    assert not exists

  @staticmethod
  def test_not_exists(testdir):
    client = Client()

    with pytest.raises(ObjectNotFoundError):
      client.delete(f"{testdir}/delete-2.txt")


  @staticmethod
  def test_not_exists_ignore_not_found(testdir):
    client = Client()
  
    result = client.delete(f"{testdir}/delete-3.txt", ignore_not_found=True)
    assert result is None


class TestDownloadAsBytes:

  @staticmethod
  def test_upload_then_download(testdir):
    client = Client()
    client.upload_from_text(f"{testdir}/download-as-bytes-1.txt",
                              TEST_FILE_CONTENTS)

    result = client.download_as_bytes(f"{testdir}/download-as-bytes-1.txt")
    assert result == bytes(TEST_FILE_CONTENTS, 'utf-8')

  @staticmethod
  def test_not_found(testdir):
    client = Client()
    with pytest.raises(ObjectNotFoundError):
      client.download_as_bytes(f"{testdir}/download-as-bytes-2.txt")


class TestDownloadAsText:

  @staticmethod
  def test_upload_then_download(testdir):
    client = Client()
    client.upload_from_text(f"{testdir}/download-as-string-1.txt",
                              TEST_FILE_CONTENTS)

    result = client.download_as_text(f"{testdir}/download-as-string-1.txt")
    assert result == TEST_FILE_CONTENTS

  @staticmethod
  def test_not_found(testdir):
    client = Client()
    with pytest.raises(ObjectNotFoundError):
      client.download_as_bytes(f"{testdir}/download-as-string-2.txt")


class TestDownloadToFilename:

  @staticmethod
  def test_upload_then_download(testdir):
    client = Client()
    client.upload_from_text(f"{testdir}/download-to-filename-1.txt",
                              TEST_FILE_CONTENTS)

    tmpdir = TemporaryDirectory()
    with tmpdir:
      client.download_to_filename(f"{testdir}/download-to-filename-1.txt",
                                  f"{tmpdir.name}/download-to-filename-1.txt")
      with open(f"{tmpdir.name}/download-to-filename-1.txt", 'r') as file:
        contents = file.read()
        assert contents == TEST_FILE_CONTENTS

  @staticmethod
  def test_not_found(testdir):
    client = Client()

    tmpdir = TemporaryDirectory()
    with tmpdir, pytest.raises(ObjectNotFoundError):
      client.download_to_filename(
        f"{testdir}/download-to-filename-2.txt",
        f"{tmpdir.name}/download-to-filename-2.txt"
      )


class TestExists:

  @staticmethod
  def test_exists(testdir):
    client = Client()
    client.upload_from_text(f"{testdir}/exists-1.txt", TEST_FILE_CONTENTS)

    exists = client.exists(f"{testdir}/exists-1.txt")
    assert exists

  @staticmethod
  def test_does_not_exist():
    client = Client()
    exists = client.exists("bad-object")
    assert not exists


class TestList:

  @staticmethod
  def test_upload_multiple_then_list(testdir):
    client = Client()
    client.upload_from_text(f"{testdir}/list/list-1-1.txt",
                              TEST_FILE_CONTENTS)
    client.upload_from_text(f"{testdir}/list/list-1-2.txt",
                              TEST_FILE_CONTENTS)
    objects = client.list(prefix=f"{testdir}/list")
    assert objects == [
        Object(name=f"{testdir}/list/list-1-1.txt"),
        Object(name=f"{testdir}/list/list-1-2.txt")
    ]


class TestUploadfromFilename:

  @staticmethod
  def test_upload_then_download(testdir):
    client = Client()

    tmpdir = TemporaryDirectory()
    with tmpdir:
      with open(f"{tmpdir.name}/upload-from-filename-1.txt", 'w') as file:
        file.write(TEST_FILE_CONTENTS)

      client.upload_from_filename(f"{testdir}/upload-from-filename-1.txt",
                                  f"{tmpdir.name}/upload-from-filename-1.txt")

    result = client.download_as_text(f"{testdir}/upload-from-filename-1.txt")
    assert result == TEST_FILE_CONTENTS


class TestUploadFromText:

  @staticmethod
  def test_upload_then_download(testdir):
    client = Client()
    client.upload_from_text(f"{testdir}/upload-from-string-1.txt",
                              TEST_FILE_CONTENTS)

    result = client.download_as_text(f"{testdir}/upload-from-string-1.txt")
    assert result == TEST_FILE_CONTENTS
