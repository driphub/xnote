# -*- coding:utf-8 -*-
# @author xupingmao <578749341@qq.com>
# @since 2020/02/16 12:49:30
# @modified 2020/02/29 01:38:11

class NoteType:

    def __init__(self, type, name):
        self.type = type
        self.name = name

NOTE_TYPE_MAPPING = {
    "document": "md",
    "text"    : "log",
    "post"    : "log",
}

NOTE_TYPE_LIST = [
    NoteType("group"  , u"项目"),
    NoteType("md"     , u"Markdown"),
    NoteType("html"   , u"富文本"),
    NoteType("csv"    , u"表格"),
    NoteType("list"   , u"清单"),
    NoteType("gallery", u"相册"),
    NoteType("log"    , u"日志"),
    NoteType("plan"   , u"计划"),
]

NOTE_TYPE_DICT = {}
# 有效的笔记类型
VALID_NOTE_TYPE_SET = set()
for item in NOTE_TYPE_LIST:
    NOTE_TYPE_DICT[item.type] = item.name
    VALID_NOTE_TYPE_SET.add(item.type)

# 其他特殊类型
NOTE_TYPE_DICT["sticky"] = u"置顶"
NOTE_TYPE_DICT["public"] = u"公共笔记"
NOTE_TYPE_DICT["removed"] = u"回收站"
NOTE_TYPE_DICT["recent_edit"] = u"最近编辑"
NOTE_TYPE_DICT["search"] = u"笔记搜索"

