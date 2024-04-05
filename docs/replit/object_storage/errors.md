# replit.object\_storage.errors

Errors that may be returned by the storage library.

## Class BucketNotFoundError

```python
class BucketNotFoundError(Exception)
```

BucketNotFoundError may occur if the specified bucket could not be found.

## Class DefaultBucketError

```python
class DefaultBucketError(Exception)
```

DefaultBucketError may occur if the default bucket could not be resolved.

## Class ForbiddenError

```python
class ForbiddenError(Exception)
```

ForbiddenError may occur if access to the requested resource is not allowed.

## Class ObjectNotFoundError

```python
class ObjectNotFoundError(Exception)
```

ObjectNotFoundError may occur if the requested object could not be found.

## Class TooManyRequestsError

```python
class TooManyRequestsError(Exception)
```

TooManyRequestsError may occur if the rate of requests exceeds the rate limit.

## Class UnauthorizedError

```python
class UnauthorizedError(Exception)
```

UnauthorizedError may occur if the requested operation is not allowed.

