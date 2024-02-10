#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Gtd232

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from urllib.request import Request, urlopen

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def aes_decrypt(bytesText: bytes) -> str:
    # CBC
    return unpad(AES.new(b'4A9745825F24883B657AFC4E4626A0F2', AES.MODE_CBC, b'4A9745825F24883B').decrypt(bytesText), AES.block_size, style='pkcs7').decode('utf-8')

def download_json(id:int,ver:int,https:bool=True) -> str:
    return aes_decrypt(urlopen(Request(f"http{'s' if https else ''}://asset.gitblock.cn/Project/download?id={id}&v={ver}",headers=headers)).read())






