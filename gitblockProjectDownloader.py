# -*- coding: utf-8 -*-
# @Author : Gtd232

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from urllib.request import Request, urlopen
from urllib.parse import unquote
import json
import os
import zipfile

headers = {
    "Accept": "*/*", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive", "Host": "asset.gitblock.cn", "Origin": "https://gitblock.cn",
    "Referer": "https://gitblock.cn/",
    "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": '"Windows"', "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}


def aes_decrypt(bytesText: bytes) -> str:
    # CBC
    return unpad(AES.new(b'4A9745825F24883B657AFC4E4626A0F2', AES.MODE_CBC, b'4A9745825F24883B').decrypt(bytesText),
                 AES.block_size, style='pkcs7').decode('utf-8')


def download_json(id: int, ver: int = 0, https: bool = True) -> str:
    """获取最新作品/未发布作品需要令ver = 0"""
    return aes_decrypt(urlopen(
        Request(
            f"http{'s' if https else ''}://asset.gitblock.cn/Project/download?id={id}{'&v=' + str(ver) if ver != 0 else ''}",
            headers=headers)).read())


def download_prj_fulldata(id: int, ver: int = 0, https: bool = True) -> dict:
    """获取最新作品/未发布作品需要令ver = 0"""
    req = urlopen(Request(
        f"http{'s' if https else ''}://asset.gitblock.cn/Project/download?id={id}{'&v=' + str(ver) if ver != 0 else ''}",
        headers=headers))
    return {
        "json": aes_decrypt(req.read()),
        "title": unquote(req.getheader("content-disposition")[29:])
    }


def download_assets(prjJson: str, path: str = "./assets", https: bool = True) -> list:
    if not os.path.exists(path):
        os.makedirs(path)
    prj = json.loads(prjJson)
    assets = []
    for sprite in prj['targets']:
        for asset in sprite['costumes']:
            assets.append(asset['md5ext'])
            with open(f"{path}/{asset['md5ext']}", 'wb') as f:
                try:
                    f.write(urlopen(
                        Request(f"http{'s' if https else ''}://asset.gitblock.cn/Project/GetAsset?name={asset['md5ext']}",
                                headers=headers)).read())
                except:
                    raise 'Download Error!'
        for asset in sprite['sounds']:
            assets.append(asset['md5ext'])
            with open(f"{path}/{asset['md5ext']}", 'wb') as f:
                try:
                    f.write(urlopen(
                        Request(f"http{'s' if https else ''}://asset.gitblock.cn/Project/GetAsset?name={asset['md5ext']}",
                                headers=headers)).read())
                except:
                    raise 'Download Error!'
    return assets


def download_assets_memory(prjJson: str, https: bool = True) -> dict:
    prj = json.loads(prjJson)
    assets = {}
    for sprite in prj['targets']:
        for asset in sprite['costumes']:
            try:
                assets[asset['md5ext']] = urlopen(
                    Request(f"http{'s' if https else ''}://asset.gitblock.cn/Project/GetAsset?name={asset['md5ext']}",
                            headers=headers)).read()
            except:
                raise 'Download Error!'
        for asset in sprite['sounds']:
            try:
                assets[asset['md5ext']] = urlopen(
                    Request(f"http{'s' if https else ''}://asset.gitblock.cn/Project/GetAsset?name={asset['md5ext']}",
                            headers=headers)).read()
            except:
                raise 'Download Error!'
    return assets


def download_sb3(id: int, ver: int = 0, fileName: str = "AUTO", https: bool = True) -> None:
    prjData = download_prj_fulldata(id, ver, https)
    prjJson = prjData["json"]
    if fileName == "AUTO":
        fileName = f"{id} - {prjData['title']}.sb3"
    assets = download_assets_memory(prjJson, https=https)
    with zipfile.ZipFile(fileName, mode="w") as archive:
        for i in assets:
            with archive.open(i, "w") as f:
                f.write(assets[i])
        archive.writestr("project.json", prjJson)
