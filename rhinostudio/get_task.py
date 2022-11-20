# SPDX-FileCopyrightText: 2022 Weibin Jia <me@isweibin.com>
# SPDX-License-Identifier: Apache-2.0

import random
import re

from Crypto.Cipher import AES
import ffmpeg
from lxml import etree
import requests

from decrypt_key import decrypt_key

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
}


def get_params(course, task):
    url = f'https://www.rhinostudio.cn/course/{course}/task/{task}/activity_show?blank=1'
    headers = {
        'Cookie': 'online-uuid=61CBCAE0-FFC9-DB29-290B-DE9636A24F1D; PHPSESSID=ubjkdce8i52d85fn049l95fhfc; REMEMBERME=Qml6XFVzZXJcQ3VycmVudFVzZXI6ZFhObGNsOXFNSFp6ZG10b2EzVkFaV1IxYzI5b2J5NXVaWFE9OjE2OTY1ODU3NDE6NzNhOGY1NTFlMzg1YWFjODZhNGFhMjdjNmZiNTM0ZDRhODBiMWUwMWYwYmNiNWQ5NTQwOTQ3ZjVmYzQ4ZThkZA%3D%3D',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    }
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    resNo = html.xpath("//div[@id='lesson-video-content']/@data-file-global-id")[0]
    token = html.xpath("//div[@id='lesson-video-content']/@data-token")[0]

    return resNo, token


def get_playlist(course, task):
    url = 'https://play.qiqiuyun.net/sdk_api/play'
    resNo, token = get_params(course, task)
    params = {
        'resNo': resNo,
        'token': token,
        'lang': 'zh-CN',
        'ssl': '1',
        'sdkType': 'js',
        'callback': 'jsonp_' + ''.join([str(random.randint(0,9)) for i in range(17)]),
    }
    response = requests.get(url, params=params)
    playlist = re.findall('"playlist":"(.*?)"', response.text)[0]

    return playlist


def get_streams(course, task):
    """Get hls definition and there correspond urls."""
    url = get_playlist(course, task)
    response = requests.get(url)
    names = re.findall('NAME=(.*)', response.text)
    streams = re.findall('https:.*', response.text)

    return names, streams


def get_task(course, task, filename):
    names, streams = get_streams(course, task)

    # Select best names.
    if '超清' in names:
        stream = streams[names.index('超清')]
    elif '高清' in names:
        stream = streams[names.index('高清')]
    else:
        stream = streams[0]

    response = requests.get(stream)
    ivs = re.findall('#EXT-X-KEY:METHOD=AES-128,URI="(https://.*)",IV=0x(.*)', response.text)[1:]
    urls = re.findall('#EXTINF:.*,\n(https://.*)', response.text)[1:]
    key = requests.get(ivs[0][0], headers=headers).text
    key = decrypt_key(key)

    # Write file.
    with open('downloads/task.ts', 'wb') as f:
        for iv, url in zip(ivs, urls):
            iv = iv[1]
            response = requests.get(url, headers=headers).content
            while len(response)%16 != 0:
                response += b"0"
            cipher = AES.new(key, AES.MODE_CBC, iv=bytes.fromhex(iv))
            f.write(cipher.decrypt(response))

    # Convert to mkv file.
    ffmpeg.input('downloads/task.ts').output(f'downloads/{filename}.mkv', map='0', codec='copy').run()
