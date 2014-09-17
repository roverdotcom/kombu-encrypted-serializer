# -*- coding: utf-8 -*-

from __future__ import absolute_import

import base64

from cryptography.fernet import Fernet

from kombu.serialization import registry, dumps, loads
from kombu.utils.encoding import bytes_to_str, str_to_bytes, ensure_bytes


def b64encode(s):
    return bytes_to_str(base64.b64encode(str_to_bytes(s)))


def b64decode(s):
    return base64.b64decode(str_to_bytes(s))


class EncryptedSerializer(object):
    def __init__(self, key=None, serializer='pickle'):
        self._key = key
        self._serializer = serializer
        self._load_codec()

        # TODO: Set this up better, catching an incorrect key
        # error and giving a better explanation in this context.
        self.fernet = Fernet(key)

    def serialize(self, data):
        content_type, content_encoding, body = dumps(
            bytes_to_str(data), serializer=self._serializer)

        return b64encode(self.encrypt(ensure_bytes(body)))

    def deserialize(self, data):
        decrypted = self.decrypt(b64decode(data))
        body = loads(
            decrypted,
            self._serializer_content_type,
            self._serializer_content_encoding,
            force=True,
        )
        return bytes_to_str(body)

    def encrypt(self, data):
        return self.fernet.encrypt(data)

    def decrypt(self, data):
        return self.fernet.decrypt(data)

    def _load_codec(self):
        codec = self._codec = registry._encoders.get(self._serializer)
        self._serializer_content_type = codec.content_type
        self._serializer_content_encoding = codec.content_encoding


def setup_encrypted_serializer(key, serializer='pickle'):
    encrypted_serializer = EncryptedSerializer(key, serializer=serializer)
    registry.register(
        'encrypted',
        encrypted_serializer.serialize,
        encrypted_serializer.deserialize,
        content_type='application/x-encrypted-serializer',
        content_encoding='utf-8',
    )
    registry._set_default_serializer('encrypted')
