"""Pythonic representation of an object in Object Storage."""

from dataclasses import dataclass


@dataclass
class Object:
  """Object contains metadata about an object."""
  name: str
