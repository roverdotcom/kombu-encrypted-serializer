# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .serialization import EncryptedSerializer
from kombu.serialization import registry

__author__ = 'Bryan Shelton'
__email__ = 'bryan@rover.com'
__version__ = '0.1.0'


def setup_encrypted_serializer(key=None, serializer='pickle', name=None):
    encrypted_serializer = EncryptedSerializer(key=key, serializer=serializer)
    if not name:
        name = "encrypted-{0}".format(serializer)
    registry.register(
        name,
        encrypted_serializer.serialize,
        encrypted_serializer.deserialize,
        content_type="application/x-{0}".format(name),
        content_encoding='utf-8',
    )
    return name
