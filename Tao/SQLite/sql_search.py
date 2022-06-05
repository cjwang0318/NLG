import sqlite3
from datetime import datetime
import random
import sys
import time
import Call_API as cs

sys.path.append("..")
import tool_box as tb


def insert_data(cursor):
    cursor.execute('''INSERT INTO synonym (key,synonym_list) VALUES ('粽子b', '粽子 肉粽 粽粽')''')
    # cursor.execute("INSERT INTO synonym VALUES('粽子', '粽子 肉粽')")
    # cursor.execute("INSERT INTO synonym VALUES('粽a', 'aaa')")
    print("ok")


def select(cursor):
    # results = cursor.execute("SELECT `key` FROM synonym WHERE `synonym_list` LIKE '%粽子%'")
    results = cursor.execute("SELECT * FROM description")
    return results


def list_shuffle(list):
    random.shuffle(list)
    return list


def get_result(cursor, query, topk):
    # print(query)
    results = cursor.execute(query)
    list = []
    for item in results:
        list.append(item[0])
    list_shuffle(list)
    if len(list) == 0:
        return None
    elif len(list) < topk:
        return list
    else:
        return list[:topk]


def generate_candidate_keyword_list(keyword):
    seg_keywords = cs.call_CKIP(keyword)
    seg_keywords_list = seg_keywords.split(" ")
    keyword_len = len(seg_keywords_list)
    i = 0
    keyword_list = []
    while i < keyword_len:
        temp = ""
        j = i
        while j < keyword_len:
            temp = temp + seg_keywords_list[j] + " "
            j = j + 1
        temp = temp.strip()
        keyword_list.append(temp)
        # print(temp)
        i = i + 1
    return seg_keywords, keyword_list


def query_construction(keyword_list):
    query = "SELECT * FROM `itemName_ID` WHERE "
    keyword_len = len(keyword_list)
    tmp = ""
    i = 1
    for item in keyword_list:
        str = "`itemName` LIKE '%" + item + "%'"
        if i < keyword_len:
            tmp = tmp + str + " AND "
        else:
            tmp = tmp + str
        i = i + 1
    return query + tmp


def generate_candidate_query_list(keyword):
    seg_keywords = cs.call_CKIP(keyword)
    keyword_list = cs.call_keyword_extraction(seg_keywords)
    keyword_len = len(keyword_list)
    i = 0
    result = []
    while i < keyword_len:
        temp = keyword_list[:keyword_len - i]
        # print(temp)
        str1 = ' '.join(temp)
        query = query_construction(temp)
        # print(query)
        result.append(str1 + "\t" + query)
        i = i + 1
    return result


def get_seg_result(cursor, keyword_list, topk):
    for keyword in keyword_list:
        # print(keyword)
        query = "SELECT `description` FROM description WHERE `description` LIKE '%" + keyword + "%'"
        results = get_result(cursor, query, topk)
        results_remove_space = []
        if results != None:
            for item in results:
                item = item.replace(" ", "")
                results_remove_space.append(item)
            return keyword, results_remove_space
    return keyword, results


def get_keyword_result(cursor, keyword_list, topk):
    for item in keyword_list:
        item_split = item.split("\t")
        keyword = item_split[0]
        query = item_split[1]
        results = get_result(cursor, query, topk)
        if results != None:
            return keyword, results
    return keyword, results


def log_results(keyword, seg_keywords, keyword_without_oov, result, generate_type):
    logList = []
    logFile = "logSQL.txt"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
    logList.append("----- " + time + " -----\n")
    logList.append("原始關鍵字：" + keyword + "\n")
    logList.append("CKIP斷詞關鍵字：" + seg_keywords + "\n")
    logList.append("進入生成系統關鍵字：" + keyword_without_oov + "\n")
    logList.append("生成模型類別：" + generate_type + "\n")
    for id, sample in enumerate(result):
        logList.append("文案" + str(id) + ":\t" + sample + "\n")
    tb.append_file(logFile, logList)


if __name__ == '__main__':
    # db = sqlite3.connect('./tao_seg_cht.db')
    # cursor = db.cursor()
    # results = select(cursor)
    # results = get_result(cursor, "bba", 3)
    # if results == None:
    #     print("no results")
    # else:
    #     print(results)
    # db.commit()
    # db.close()
    start = time.time()
    # seg_keywords, keyword_list = generate_candidate_keyword_list("超級無敵馬甲西裝")
    seg_keywords = generate_candidate_query_list("超級無敵馬甲西裝")
    print(seg_keywords)
    # print(keyword_list)
    # keyword, ans = get_seg_result(cursor, keyword_list, 5)
    end = time.time()
    print('time: ', end - start)
