#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : Gtd232

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from urllib.request import Request, urlopen
import json
import os
import zipfile

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def aes_decrypt(bytesText: bytes) -> str:
    # CBC
    return unpad(AES.new(b'4A9745825F24883B657AFC4E4626A0F2', AES.MODE_CBC, b'4A9745825F24883B').decrypt(bytesText), AES.block_size, style='pkcs7').decode('utf-8')

def download_json(id:int,ver:int,https:bool=True) -> str:
    return aes_decrypt(urlopen(Request(f"http{'s' if https else ''}://asset.gitblock.cn/Project/download?id={id}&v={ver}",headers=headers)).read())

def download_assets(prjJson:str, path:str="./assets", https:bool=True) -> list:
    if not os.path.exists(path):
        os.makedirs(path)
    prj = json.loads(prjJson)
    assets = []
    for sprite in prj['targets']:
        for asset in sprite['costumes']:
            assets.append(asset['md5ext'])
            with open(f"{path}/{asset['md5ext']}", 'wb') as f:
                try:
                    f.write(urlopen(Request(f"http{'s' if https else ''}://cdn.gitblock.cn/Project/GetAsset?name={asset['md5ext']}", headers=headers)).read())
                except:
                    raise 'Download Error!'
        for asset in sprite['sounds']:
            assets.append(asset['md5ext'])
            with open(f"{path}/{asset['md5ext']}", 'wb') as f:
                try:
                    f.write(urlopen(Request(f"http{'s' if https else ''}://cdn.gitblock.cn/Project/GetAsset?name={asset['md5ext']}", headers=headers)).read())
                except:
                    raise 'Download Error!'
    return assets

def download_assets_memory(prjJson:str, https:bool=True) -> dict:
    prj = json.loads(prjJson)
    assets = {}
    for sprite in prj['targets']:
        for asset in sprite['costumes']:
            try:
                assets[asset['md5ext']] = urlopen(Request(f"http{'s' if https else ''}://cdn.gitblock.cn/Project/GetAsset?name={asset['md5ext']}", headers=headers)).read()
            except:
                raise 'Download Error!'
        for asset in sprite['sounds']:
            try:
                assets[asset['md5ext']] = urlopen(Request(f"http{'s' if https else ''}://cdn.gitblock.cn/Project/GetAsset?name={asset['md5ext']}", headers=headers)).read()
            except:
                raise 'Download Error!'
    return assets

def download_sb3(id:int,ver:int, fileName:str="project.sb3",https:bool=True) -> None:
    prjJson = download_json(id,ver,https)
    assets = download_assets_memory(prjJson,https=https)
    with zipfile.ZipFile(fileName, mode="w") as archive:
        for i in assets:
            with archive.open(i, "w") as f:
                f.write(assets[i])
        archive.writestr("project.json", prjJson)







