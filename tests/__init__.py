# -*- coding: utf-8 -*-

import unittest

from cryptography.fernet import Fernet

TEST_KEY = Fernet.generate_key()


class KombuEncryptionTestCase(unittest.TestCase):
    def setUp(self):
        self.key = TEST_KEY
