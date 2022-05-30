import sqlite3
from datetime import datetime
import random
import sys
import time
import CKIP as cs

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


def get_result(cursor, keyword, topk):
    query = "SELECT `description` FROM description WHERE `description` LIKE '%" + keyword + "%'"
    # query = "SELECT * FROM description WHERE `description` LIKE 'qq'"
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


def get_seg_result(cursor, keyword_list, topk):
    for keyword in keyword_list:
        # print(keyword)
        results = get_result(cursor, keyword, topk)
        results_remove_apace = []
        if results != None:
            for item in results:
                item = item.replace(" ", "")
                results_remove_apace.append(item)
            return keyword, results_remove_apace
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
    db = sqlite3.connect('./tao_seg_cht.db')
    cursor = db.cursor()
    # results = select(cursor)
    # results = get_result(cursor, "bba", 3)
    # if results == None:
    #     print("no results")
    # else:
    #     print(results)
    # db.commit()
    # db.close()
    start = time.time()
    seg_keywords, keyword_list = generate_candidate_keyword_list("超級無敵馬甲西裝")
    print(seg_keywords)
    # print(keyword_list)
    keyword, ans = get_seg_result(cursor, keyword_list, 5)
    end = time.time()
    print('time: ', end - start)
    print(keyword)
    print(ans)
