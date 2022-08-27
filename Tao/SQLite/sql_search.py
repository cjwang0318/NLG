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


def query_construction_desc_only(keyword_list):
    query = "SELECT `description` FROM `description` WHERE "
    keyword_len = len(keyword_list)
    tmp = ""
    i = 1
    for item in keyword_list:
        str = "`description` LIKE '%" + item + "%'"
        if i < keyword_len:
            tmp = tmp + str + " AND "
        else:
            tmp = tmp + str
        i = i + 1
    return query + tmp


def query_construction_item_desc(keyword_list):
    query = "SELECT `description` FROM `item_desc_cht` WHERE "
    keyword_len = len(keyword_list)
    tmp_item = ""
    tmp_desc = ""
    i = 1
    for item in keyword_list:
        str_item = "`itemName` LIKE '%" + item + "%'"
        str_desc = "`description` LIKE '%" + item + "%'"
        if i < keyword_len:
            tmp_item = tmp_item + str_item + " AND "
            tmp_desc = tmp_desc + str_desc + " AND "
        else:
            tmp_item = tmp_item + str_item
            tmp_desc = tmp_desc + str_desc
        i = i + 1
    # OR_operation=query + "(" + tmp_item + ") OR (" + tmp_desc + ")"
    AND_operation = query + "(" + tmp_item + ") AND (" + tmp_desc + ")"
    return AND_operation


def generate_candidate_query_list(keyword, nkeywords):
    seg_keywords = cs.call_CKIP(keyword)
    seg_keywords_list = seg_keywords.split(" ")
    num_keywords = len(seg_keywords_list)
    # 如果斷詞後字數大於閥值才會呼叫關鍵字擷取API
    if num_keywords > nkeywords:
        keyword_list = cs.call_keyword_extraction(seg_keywords)
        # 如果關鍵詞擷取沒有作用，例如輸入『[還 活 著 嗎』，就使用沒有斷詞的keyword
        if len(keyword_list) == 0:
            keyword_list.append(keyword)
        # 將關鍵詞擷取後的結果加到seg_keywords
        seg_keywords = seg_keywords + "=>關鍵詞擷取結果[" + ', '.join(keyword_list) + "]"
    else:
        # 將keyword_list中的元素倒排序，因為最重要的字(名詞)可能會再最後面
        seg_keywords_list.reverse()
        keyword_list = seg_keywords_list
    keyword_len = len(keyword_list)
    i = 0
    result = []
    while i < keyword_len:
        temp = keyword_list[:keyword_len - i]
        # print(temp)
        str1 = ' '.join(temp)
        # 只搜尋description
        # query = query_construction_desc_only(temp)
        # 同時搜尋itemName & description
        query = query_construction_item_desc(temp)
        # print(query)
        result.append(str1 + "\t" + query)
        i = i + 1
    return seg_keywords, result


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
    # 若第1個SQL query搜尋數量不足，就會持續使用第2個SQL query，直到滿足搜尋數量為止
    sql_search_keyword = ""
    joined_results = []
    for item in keyword_list:
        item_split = item.split("\t")
        keyword = item_split[0]
        query = item_split[1]
        results = get_result(cursor, query, topk)
        if results != None:
            num_results = len(results)
            sql_search_keyword = sql_search_keyword + keyword + "(" + str(num_results) + "),"
            joined_results = joined_results + results
            topk = topk - num_results
            if topk == 0:
                sql_search_keyword = sql_search_keyword[:-1]
                list_shuffle(joined_results)
                return sql_search_keyword, joined_results
    return keyword, results


def log_results(keyword, seg_keywords, keyword_without_oov, result, generate_type, category):
    logList = []
    logFile = "log.txt"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
    logList.append("----- " + time + " -----\n")
    logList.append("原始關鍵字：" + keyword + "\n")
    logList.append("CKIP斷詞關鍵字：" + seg_keywords + "\n")
    logList.append("進入生成系統關鍵字：" + keyword_without_oov + "\n")
    logList.append("生成模型類型：" + generate_type + "\n")
    logList.append("生成模型類別：" + str(category) + "\n")
    for id, sample in enumerate(result):
        logList.append("文案" + str(id) + ":\t" + sample + "\n")
    tb.append_file(logFile, logList)


if __name__ == '__main__':
    db = sqlite3.connect('./tao_item_desc_cht.db')
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
    # seg search testing
    # seg_keywords, keyword_list = generate_candidate_keyword_list("超級無敵馬甲西裝")
    # print(keyword_list)
    # keyword, ans = get_seg_result(cursor, keyword_list, 5)
    # print(keyword)
    # print(ans)

    # keyword search testing
    # seg_keywords, keyword_query = generate_candidate_query_list("樂活e棧-聖誕節MIT豪華加厚禦寒版-聖誕老人服裝(豪華5件套組)", 3)
    # seg_keywords, keyword_query = generate_candidate_query_list("野生白蝦", 3)
    # seg_keywords, keyword_query = generate_candidate_query_list("還活著嗎", 3)
    seg_keywords, keyword_query = generate_candidate_query_list("貼身牛仔褲", 3)
    print(seg_keywords)
    print(keyword_query)
    sql_search_keyword, results = get_keyword_result(cursor, keyword_query, 5)
    print(sql_search_keyword)
    print(results)
    end = time.time()
    print('time: ', end - start)
