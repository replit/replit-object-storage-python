# replit-object-storage-python
The library for interacting with Replit's Object Storage service, on Replit.

## Usage

### Setup

Start by importing the Object Storage Client:
```python
from replit.object_storage import Client
```

Then to use the Client:
```python
client = Client()
```

### Downloading an Object

```python
contents = client.download_as_text("file.json")
```

### Uploading an Object

```python
client.upload_from_text("file.json", data)
```

### List Objects

```python
client.list()
```

### Delete an Object

```python
contents = client.delete("file.json")
```
