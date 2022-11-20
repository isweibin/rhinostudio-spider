# SPDX-FileCopyrightText: 2022 Weibin Jia <me@isweibin.com>
# SPDX-License-Identifier: Apache-2.0

from get_task import get_task


def get_course(course, data):
    dirname = None
    for _ in data:
        if _['type'] == 'video':
            filename = f"{_['number']}-{_['title']}"
            get_task(course, _['taskId'], filename)
