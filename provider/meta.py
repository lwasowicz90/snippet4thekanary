"""Helper module to store provider data"""
from dataclasses import dataclass


@dataclass
class MetaProvider:
    """For storing data"""
    url: str
    tag: str
    attrs: dict
