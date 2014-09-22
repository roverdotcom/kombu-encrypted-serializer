# -*- coding: utf-8 -*-

from __future__ import absolute_import

from mock import patch, MagicMock

from . import KombuEncryptionTestCase

from kombu_encrypted_serializer import setup_encrypted_serializer


class SetupEncryptedSerializerTests(KombuEncryptionTestCase):
    def setUp(self):
        super(SetupEncryptedSerializerTests, self).setUp()
        ec = 'kombu_encrypted_serializer.EncryptedSerializer'
        self.ec_patcher = patch(ec)
        self.register_patcher = patch('kombu.serialization.registry.register')
        self.encrypted_serializer_mock = self.ec_patcher.start()
        self.register_mock = self.register_patcher.start()

        self.encrypted_serializer_mock_instance = MagicMock()
        self.encrypted_serializer_mock.return_value = (
            self.encrypted_serializer_mock_instance)

    def tearDown(self):
        self.register_patcher.stop()
        self.ec_patcher.stop()

    def test_passes_args_to_serializer_init(self):
        setup_encrypted_serializer(self.key)
        self.assertEqual(1, self.register_mock.call_count)
        self.encrypted_serializer_mock.assert_called_once_with(
            key=self.key,
            serializer='pickle',
        )

    def test_calls_kombu_registry_register(self):
        setup_encrypted_serializer(self.key)
        self.assertEqual(1, self.register_mock.call_count)

    def test_can_override_serializer_name(self):
        name = setup_encrypted_serializer(self.key, name='new-name')
        self.assertEqual(name, 'new-name')
        self.register_mock.assert_called_once_with(
            'new-name',
            self.encrypted_serializer_mock_instance.serialize,
            self.encrypted_serializer_mock_instance.deserialize,
            content_type='application/x-new-name',
            content_encoding='utf-8',
        )

    def test_name_reflects_serializer_by_default(self):
        name = setup_encrypted_serializer(self.key, serializer='json')
        self.assertEqual(name, 'encrypted-json')
        self.register_mock.assert_called_once_with(
            'encrypted-json',
            self.encrypted_serializer_mock_instance.serialize,
            self.encrypted_serializer_mock_instance.deserialize,
            content_type='application/x-encrypted-json',
            content_encoding='utf-8',
        )

    def test_kombu_serializer_registration(self):
        setup_encrypted_serializer(key=self.key, serializer='pickle')
        self.register_mock.assert_called_once_with(
            'encrypted-pickle',
            self.encrypted_serializer_mock_instance.serialize,
            self.encrypted_serializer_mock_instance.deserialize,
            content_type='application/x-encrypted-pickle',
            content_encoding='utf-8',
        )
