# replit.object\_storage.client

Client for interacting with Object Storage. This is the top-level interface.

Note: this Client is a thin wrapper over the GCS Python Library. As a result,
many docstrings are borrowed from the underlying library.

## Class Client

```python
class Client()
```

Client manages interactions with Replit Object Storage.

If multiple buckets are used within an application, one Client should be used
per bucket

Any method may return one of the following errors:
- `BucketNotFoundError`: If the bucket configured for the client could not be found.
- `DefaultBucketError`: If no bucket was explicitly configured and an error occurred
    when resolving the default bucket.
- `ForbiddenError`: If access to the requested resource is not allowed.
- `TooManyRequestsError`: If rate limiting occurs.
- `UnauthorizedError`: If the requested operation is not allowed.

#### \_\_init\_\_

```python
def __init__(bucket_id: Optional[str] = None)
```

Creates a new Client.

**Arguments**:

- `bucket_id` - The ID of the bucket this Client should interface with.
  If no ID is defined, the Repl / Deployment&#x27;s default bucket will be
  used.

#### copy

```python
def copy(object_name: str, dest_object_name: str) -> None
```

Copies the specified object within the same bucket.

If an object exists in the same location, it will be overwritten.

**Arguments**:

- `object_name` - The full path of the object to be copied.
- `dest_object_name` - The full path to copy the object to.
  

**Raises**:

- `ObjectNotFoundError` - If the source object could not be found.

#### delete

```python
def delete(object_name: str, ignore_not_found: bool = False) -> None
```

Deletes an object from Object Storage.

**Arguments**:

- `object_name` - The name of the object to be deleted.
- `ignore_not_found` - Whether an error should be raised if the object does not
  exist.
  

**Raises**:

- `ObjectNotFoundError` - If the object could not be found.

#### download\_as\_bytes

```python
def download_as_bytes(object_name: str) -> bytes
```

Download the contents an object as a bytes object.

**Arguments**:

- `object_name` - The name of the object to be downloaded.
  

**Returns**:

  The raw byte representation of the object&#x27;s contents.
  

**Raises**:

- `ObjectNotFoundError` - If the object could not be found.

#### download\_as\_text

```python
def download_as_text(object_name: str) -> str
```

Download the contents an object as a string.

**Arguments**:

- `object_name` - The name of the object to be downloaded.
  

**Returns**:

  The object&#x27;s contents as a UTF-8 encoded string.
  

**Raises**:

- `ObjectNotFoundError` - If the object could not be found.

#### download\_to\_filename

```python
def download_to_filename(object_name: str, dest_filename: str) -> None
```

Download the contents an object into a file on the local disk.

**Arguments**:

- `object_name` - The name of the object to be downloaded.
- `dest_filename` - The filename of the file on the local disk to be written.
  

**Raises**:

- `ObjectNotFoundError` - If the object could not be found.

#### exists

```python
def exists(object_name: str) -> bool
```

Checks if an object exist.

**Arguments**:

- `object_name` - The name of the object to be checked.
  

**Returns**:

  Whether or not the object exists.

#### list

```python
def list(end_offset: Optional[str] = None,
         match_glob: Optional[str] = None,
         max_results: Optional[int] = None,
         prefix: Optional[str] = None,
         start_offset: Optional[str] = None) -> List[Object]
```

Lists objects in the bucket.

**Arguments**:

- `end_offset` - Filter results to objects whose names are lexicographically
  before end_offset. If start_offset is also set, the objects listed
  have names between start_offset (inclusive) and end_offset
  (exclusive).
- `match_glob` - Glob pattern used to filter results, for example foo*bar.
- `max_results` - The maximum number of results that can be returned in the
  response.
- `prefix` - Filter results to objects who names have the specified prefix.
- `start_offset` - Filter results to objects whose names are
  lexicographically equal to or after start_offset. If endOffset is
  also set, the objects listed have names between start_offset
  (inclusive) and end_offset (exclusive).
  

**Returns**:

  A list of objects matching the given query parameters.

#### upload\_from\_filename

```python
def upload_from_filename(dest_object_name: str, src_filename: str) -> None
```

Upload an object from a file on the local disk.

**Arguments**:

- `dest_object_name` - The name of the object to be uploaded.
- `src_filename` - The filename of a file on the local disk

#### upload\_from\_bytes

```python
def upload_from_bytes(dest_object_name: str, src_data: bytes) -> None
```

Upload an object from bytes.

**Arguments**:

- `dest_object_name` - The name of the object to be uploaded.
- `src_data` - The bytes to be uploaded.

#### upload\_from\_text

```python
def upload_from_text(dest_object_name: str, src_data: Union[bytes,
                                                            str]) -> None
```

Upload an object from a string.

**Arguments**:

- `dest_object_name` - The name of the object to be uploaded.
- `src_data` - The text to be uploaded.

