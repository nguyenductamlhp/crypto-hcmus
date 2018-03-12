# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.addons.website.models.website import slug
import string
from datetime import datetime

import sys, getopt, os, struct
from Crypto.Cipher import AES
from Crypto.Hash import MD5, SHA256
from Crypto import Random
import  Crypto.Util.Counter
import base64
import hashlib

class EncryptDecrypt(models.Model):

    _name = 'encrypt.decrypt'

    name = fields.Char("Name", required=True)
    mode = fields.Selection(
        string="Mode",
        selection=[
            ('ecb', 'ECB'),
            ('cfb', 'CFB'),
            ('ofb', 'OFB'),
            ('cbc', 'CBC'),
            ('ctr', 'CTR'),
        ]
    )
    bs = fields.Integer("BS", default=32)
    key = fields.Char("Key", required=True)
    text_encrypt = fields.Text("Text Encrypt")
    text_decrypt = fields.Text("Text Decrypt")

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


    def encrypt_text(self):
        print self
        if not self.text_encrypt:
            return None
        mode = None
        if self.mode == 'ecb':
            mode = AES.MODE_ECB
        elif self.mode == 'cfb':
            mode = AES.MODE_CFB
        elif self.mode == 'ofb':
            mode = AES.MODE_OFB
        elif self.mode == 'cbc':
            mode =  AES.MODE_CBC
        elif self.mode == 'ctr':
            mode = AES.MODE_CTR
        if not mode:
            return
        key = hashlib.sha256(self.key.encode()).digest()

        print ">>> self.key", self.key, len(self.key), sys.getsizeof(self.key)
        raw = self._pad(self.text_encrypt)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        self.text_decrypt = base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt_text(self):
        key = hashlib.sha256(self.key.encode()).digest()
        enc = base64.b64decode(self.text_decrypt)
        iv = enc[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        self.text_encrypt = self._unpad(self, cipher.decrypt(enc[AES.block_size:])).decode('utf-8')