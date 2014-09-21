# -*- coding: utf-8 -*-

from __future__ import absolute_import

import unittest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from . import KombuEncryptionTestCase

from cryptography.fernet import InvalidToken

from kombu_encrypted_serializer.serialization import EncryptedSerializer


class SerializationTestsBase(object):
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


class JsonSerializationTests(SerializationTestsBase, KombuEncryptionTestCase):
    def setUp(self):
        super(JsonSerializationTests, self).setUp()
        self.serializer = EncryptedSerializer(
            key=self.key, serializer='json')


class PickleSerializationTests(
        SerializationTestsBase, KombuEncryptionTestCase):
    def setUp(self):
        super(PickleSerializationTests, self).setUp()
        self.serializer = EncryptedSerializer(
            key=self.key, serializer='pickle')


class MsgpackSerializationTests(
        SerializationTestsBase, KombuEncryptionTestCase):
    def setUp(self):
        super(MsgpackSerializationTests, self).setUp()
        self.serializer = EncryptedSerializer(
            key=self.key, serializer='msgpack')


class YamlSerializationTests(SerializationTestsBase, KombuEncryptionTestCase):
    def setUp(self):
        super(YamlSerializationTests, self).setUp()
        self.serializer = EncryptedSerializer(
            key=self.key, serializer='yaml')


class TestEncryptedSerializer(KombuEncryptionTestCase):
    @patch.dict('os.environ', {
        "KOMBU_ENCRYPTED_SERIALIZER_KEY": 'KEY',
    })
    @patch("kombu_encrypted_serializer.serialization.Fernet")
    def test_key_is_passed_from_an_environment_variable(self, fernet_mock):
        e = EncryptedSerializer()
        fernet_mock.assert_called_with('KEY')
        self.assertEqual(e._key, 'KEY')


if __name__ == '__main__':
    unittest.main()
