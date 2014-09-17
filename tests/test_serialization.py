# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest

from . import KombuEncryptionTestCase

from cryptography.fernet import Fernet, InvalidToken

from kombu_encrypted_serializer.serialization import EncryptedSerializer


class TestSerializationBase(object):

    def setUp(self):
        super(TestSerializationBase, self).setUp()
        self.key = Fernet.generate_key()
        self.serializer = EncryptedSerializer(key=self.key)

    def _serialize_deserialize(self, data):
        serialized = self.serializer.serialize(data)
        return self.serializer.deserialize(serialized)

    def test_serialize_and_deserialize(self):
        data = {'test': 'data', 'hello': 'wow', 'num': 12}
        out = self._serialize_deserialize(data)
        self.assertEqual(out, data)
        self.assertEqual(out['num'], 12)
        self.assertTrue(isinstance(out['num'], int))

    def test_serialize_and_deserialize_boolean(self):
        data = False
        out = self._serialize_deserialize(data)
        self.assertEqual(out, False)
        self.assertTrue(isinstance(out, bool))

    def test_raises_security_error(self):
        self.assertRaises(InvalidToken, self.serializer.deserialize, 'blah')


class TestJsonSerialization(TestSerializationBase, KombuEncryptionTestCase):
    def setUp(self):
        super(TestJsonSerialization, self).setUp()
        self.serializer = EncryptedSerializer(
            key=self.key, serializer='json')


class TestPickleSerialization(TestSerializationBase, KombuEncryptionTestCase):
    def setUp(self):
        super(TestPickleSerialization, self).setUp()
        self.serializer = EncryptedSerializer(
            key=self.key, serializer='pickle')


class TestMsgpackSerialization(TestSerializationBase, KombuEncryptionTestCase):
    def setUp(self):
        super(TestMsgpackSerialization, self).setUp()
        self.serializer = EncryptedSerializer(
            key=self.key, serializer='msgpack')


class TestYamlSerialization(TestSerializationBase, KombuEncryptionTestCase):
    def setUp(self):
        super(TestYamlSerialization, self).setUp()
        self.serializer = EncryptedSerializer(
            key=self.key, serializer='yaml')


if __name__ == '__main__':
    unittest.main()
