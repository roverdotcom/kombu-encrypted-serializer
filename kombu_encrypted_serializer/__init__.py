# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .serialization import EncryptedSerializer
from kombu.serialization import registry

__author__ = 'Bryan Shelton'
__email__ = 'bryan@rover.com'
__version__ = '0.1.0'


def setup_encrypted_serializer(key=None, serializer='pickle'):
    encrypted_serializer = EncryptedSerializer(key=key, serializer=serializer)
    registry.register(
        'encrypted',
        encrypted_serializer.serialize,
        encrypted_serializer.deserialize,
        content_type='application/x-encrypted-serializer',
        content_encoding='utf-8',
    )
