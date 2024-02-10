#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Gtd232

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

def aes_decrypt(text):
    # CBC
    return unpad(AES.new(b'4A9745825F24883B657AFC4E4626A0F2', AES.MODE_CBC, b'4A9745825F24883B').decrypt(base64.b64decode(text.encode())),AES.block_size,'pkcs7').decode('utf-8')





