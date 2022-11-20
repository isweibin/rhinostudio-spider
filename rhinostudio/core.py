# SPDX-FileCopyrightText: 2022 Weibin Jia <me@isweibin.com>
# SPDX-License-Identifier: Apache-2.0

import html
import json
import re

from lxml import etree
import requests

from get_course import get_course
from get_task import get_task


def get_data(course):
    url = f'https://www.rhinostudio.cn/course/{course}/task/list/render/default'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    }
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    data = html.xpath("//div[@class='hidden js-hidden-cached-data']/text()")[0].strip()
    data = json.loads(data)

    return data


def main():
    course = input('Course ID: ')
    task = input('Task ID: ')

    data = get_data(course)
    if task:
        for _ in data:
            if task == _['taskId']:
                filename = f"{_['number']}-{_['title']}"
        get_task(course, task, filename)
    else:
        get_course(course, data)


if __name__ == '__main__':
    main()
