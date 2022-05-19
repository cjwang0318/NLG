import random
import tool_box as tb
from datetime import datetime
from opencc import OpenCC


def convert_s2tw(str):
    cc = OpenCC('s2twp')  # convert from Simplified Chinese to Traditional Chinese
    converted = cc.convert(str)
    return converted


def load_data(dictionary_path):
    lines = tb.read_file(dictionary_path, 0)
    sentenceList = []
    pre_keyword = ""
    dict = {}
    for line in lines:
        temp = line.split("\t")
        keyword = temp[0]

        if (keyword == pre_keyword or pre_keyword == ""):
            sentenceList.append(temp[1])
            pre_keyword = keyword
        else:
            dict[pre_keyword] = sentenceList
            sentenceList = []
            pre_keyword = keyword
            sentenceList.append(temp[1])
    dict[pre_keyword] = sentenceList
    return dict


def in_dictionary(keyword, dict):
    if keyword in dict:
        return True
    else:
        return False


def list_shuffle(list):
    random.shuffle(list)
    return list


def list_fetch_top_K(list, top_k):
    length = len(list)
    if length < top_k:
        return list
    else:
        return list[:top_k]


def dictionary_search_check(keyword, dict, threshold):
    dict_prob = random.random()  # 隨機產生一個機率，若大於threshold才會使用字典回傳
    # print(dict_prob)
    keyword = convert_s2tw(keyword)
    keyword = keyword.replace(" ", "")
    if dict_prob < threshold:
        return False
    flag = in_dictionary(keyword, dict)
    if flag == True:
        return True
    else:
        return False


def dictionary_search_rest(dict, keyword, seg_keywords, keyword_without_oov, nsamples, generate_type):
    keyword_without_oov = convert_s2tw(keyword_without_oov)
    result = dict.get(keyword_without_oov)
    list_shuffle(result)
    result = list_fetch_top_K(result, nsamples)
    log_results(keyword, seg_keywords, keyword_without_oov, result, generate_type)
    answer = {"keyword": str(keyword_without_oov), "nsamples": str(nsamples), "samples": result}
    return answer


def log_results(keyword, seg_keywords, keyword_without_oov, result, generate_type):
    logList = []
    logFile = "log.txt"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
    logList.append("----- " + time + " -----\n")
    logList.append("原始關鍵字：" + keyword + "\n")
    logList.append("CKIP斷詞關鍵字：" + seg_keywords + "\n")
    logList.append("進入生成系統關鍵字：" + keyword_without_oov + "\n")
    logList.append("生成模型類別：" + generate_type + "\n")
    for id, sample in enumerate(result):
        logList.append("文案" + str(id) + ":\t" + sample + "\n")
    tb.append_file(logFile, logList)


"""
1. 判斷關鍵字是否有在字典檔
2. 若無：呼叫GPT2模組自動生成文案
3. 如果在字典檔，亂數產生一個機率值
4. 如機率於大於某個門檻，就直接使用文案庫中的文案，反之就呼叫GPT2模組自動生成文案
5. 整理文案庫
"""
if __name__ == '__main__':
    dict = load_data("./dict/description.txt")
    threshold = 0.01
    nsamples = 5
    keyword = "時尚風西裝"
    seg_keywords = "時尚風 西裝"
    seg_keyword_without_oov = "時尚風西裝"
    dict_prob = random.random()
    flag = dictionary_search_check(keyword, dict, threshold)
    print(flag)
    if flag:
        generate_type = "DICT"
        answer = dictionary_search_rest(dict, keyword, seg_keywords, seg_keyword_without_oov, nsamples, generate_type)
        print(answer)
    else:
        print("flag=" + str(flag))
        print("call GPT")
