# -*- coding:utf-8 -*-  
# Created by xupingmao on 2017/06/11
# @modified 2019/02/16 12:49:38

"""英汉、汉英词典

dictDTB结构
    _id integer primary key autoincrement,
    en text,cn text,
    symbol text 指音标

"""
import re
import os
import xutils
import xmanager
import xconfig
import xtables
from xutils import u, Storage, SearchResult, textutil

def wrap_results(dicts, origin_key):
    files = []
    for f0 in dicts:
        f = SearchResult()
        f.key = u(f0["key"])
        f.category = "dict"
        f.name = u("翻译 - ") + u(f0[origin_key])
        f.raw = f0["value"].replace("\\n", "\n")
        f.url = "#"
        files.append(f)
    return files

def search(ctx, word):
    """英汉翻译"""
    word = word.lower()
    path = os.path.join(xconfig.DATA_PATH, "dictionary.db")
    if not os.path.exists(path):
        return []
    # COLLATE NOCASE是sqlite的方言
    # 比较通用的做法是冗余字段
    sql = "SELECT * FROM dictTB WHERE en=? COLLATE NOCASE"
    dicts = xutils.db_execute(path, sql, (word,))
    return wrap_results(dicts, "en")

# \u7ffb\u8bd1 翻译
# \u5b9a\u4e49 定义
@xmanager.searchable(r"(翻译|定义|define|def|translate)\s+([^\s]+)")
def do_translate(ctx):
    key  = ctx.key
    word = ctx.groups[1]
    word = word.strip().lower()
    path = os.path.join(xconfig.DATA_PATH, "dictionary.db")
    if not os.path.exists(path):
        return
    user_name = ctx.user_name
    table     = xtables.get_dict_table()
    if textutil.isalpha(word):
        dicts = table.select(where="key LIKE $key",
            vars = dict(key = word + '%'))
    else:
        dicts = table.select(where="value LIKE $value", 
            vars = dict(value = '%' + word + '%', user = user_name))
    ctx.dicts += wrap_results(dicts, "key")

@xmanager.searchable(r"[a-zA-Z\-]+")
def translate_english(ctx):
    """使用词库进行部分模糊匹配"""
    if not ctx.search_dict:
        return
    if not xconfig.DEV_MODE:
        return
    user_name = ctx.user_name
    db = xtables.get_dictionary_table()
    results = db.select(where="key like $key AND (user=$user OR user='')", vars=dict(key=ctx.input_text + "%", user=user_name))
    for item in results:
        value = item.value.replace("\\n", "\n")
        ctx.dicts.append(Storage(name=u("翻译 - %s") % item.key, key = item.key,
            raw = value, url = "#", category = "dict"))



