# install opencc
# pip install opencc-python-reimplemented
from opencc import OpenCC
import tool_box
import re
from datetime import datetime


def convert_s2c(str):
    cc = OpenCC('s2twp')  # convert from Simplified Chinese to Traditional Chinese
    converted = cc.convert(str)
    return converted


def chinese_sentence_search(index_template, str):
    match_object = tool_box.chinese_sentence_index(index_template, str)
    indexStr = 0
    # print(match_object)
    if match_object:
        lastIndex = len(match_object)
        span = match_object[lastIndex - 1].span()
        indexStr = span[0]
    else:
        indexStr = -1
    return indexStr


def chinese_post_processing_to_file(dataList, chinese_search_template):
    result = []
    for line in dataList:
        convertedLine = convert_s2c(line)
        chineseCheck = tool_box.check_contain_chinese(convertedLine)
        if "==========================================================================================" in convertedLine:
            result.append(convertedLine + "\n\n")
        elif "========================================" in convertedLine:
            result.append(convertedLine + "\n")
        elif chineseCheck == None:
            continue
        else:
            index = chinese_sentence_search(chinese_search_template, convertedLine)
            cut_sentence = convertedLine[:index] + "。\n"
            result.append(cut_sentence)
            # print(cut_sentence)
    return result


def chinese_post_processing_to_api(dataList, chinese_search_template):
    result = []
    sampleStr = ""
    for line in dataList:
        convertedLine = convert_s2c(line)
        chineseCheck = tool_box.check_contain_chinese(convertedLine)
        if "==========================================================================================" in convertedLine:
            index = chinese_sentence_search(chinese_search_template, sampleStr)  # 將句子的最後一個字改成句點，並將多餘的部分去除
            cut_sentence = sampleStr[:index] + "。"
            result.append(cut_sentence)
            sampleStr = ""

        elif "========================================" in convertedLine:
            # result.append(convertedLine+"\n")
            continue
        elif chineseCheck == None:
            continue
        else:
            sampleStr = sampleStr + convertedLine
    return result


def remove_keyword(keyword, str):
    if keyword + "，" in str:
        str_without_keyword = str.replace(keyword + "，", "")
    elif keyword + "。" in str:
        str_without_keyword = str.replace(keyword + "。", "")
    else:
        str_without_keyword = str
    return str_without_keyword


def remove_last_sentence(str):
    strList = str.split("。")
    num_of_sentence = len(strList)
    if (num_of_sentence != 2):
        i = 0
        str_without_last_sentence = ""
        while i < num_of_sentence - 2:
            str_without_last_sentence = str_without_last_sentence + strList[i] + "。"
            i = i + 1
    else:
        str_without_last_sentence = str
    return str_without_last_sentence


def remove_duplicated_sub_sentence(str):
    stnList = str.split("。")
    no_duplicated_sentence = ""
    for sentence in stnList:
        if (sentence == ""):
            continue
        if ("，" not in sentence):
            no_duplicated_sentence = no_duplicated_sentence + sentence + "。"
            continue
        strList = sentence.split("，")
        num_sub_strList = len(strList)
        for i, element in enumerate(strList):
            if (i < num_sub_strList - 1):
                check_str = strList[i + 1]
            else:
                no_duplicated_sentence = no_duplicated_sentence + element + "。"
                continue
            if (element == check_str):
                continue
            else:
                no_duplicated_sentence = no_duplicated_sentence + element + "，"
    return no_duplicated_sentence


def getResult(keyword, seg_keywords, keyword_without_oov, nsamples, generate_type):
    chinese_search_template = '，。！'
    dataPath = "./output/"
    readFile = "samples.txt"
    logFile = "log.txt"
    data = tool_box.read_file(dataPath + readFile, 0)
    result = chinese_post_processing_to_api(data, chinese_search_template)
    # print(result)
    keyword_without_oov = convert_s2c(keyword_without_oov)
    # transform to json format
    ans = {"keyword": str(keyword), "nsamples": str(nsamples)}
    sampleList = []
    logList = []
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
    logList.append("----- " + time + " -----\n")
    logList.append("原始關鍵字：" + keyword + "\n")
    logList.append("CKIP斷詞關鍵字：" + seg_keywords + "\n")
    logList.append("進入生成系統關鍵字：" + keyword_without_oov + "\n")
    logList.append("生成模型類別：" + generate_type + "\n")
    for id, sample in enumerate(result):
        # print(id)
        # sampleID = "sample_" + str(id)
        # ans[sampleID] = sample
        sample = remove_keyword(keyword_without_oov, sample)  # remove prefix in the return sentence
        sample = remove_last_sentence(sample)  # remove last sentence
        sample = remove_duplicated_sub_sentence(sample)  # remove same words in a sentence
        logList.append("文案" + str(id) + ":\t" + sample + "\n")
        sample = sample.replace("[UNK]", "")
        sampleList.append(sample)
    tool_box.append_file(logFile, logList)
    ans["samples"] = sampleList
    return ans


if __name__ == '__main__':
    chinese_search_template = '，。！'
    dataPath = "./output/"
    readFile = "samples.txt"
    writeFile = "results.txt"
    # data = tool_box.read_file(dataPath + readFile, 0)
    str1 = '天空是有些阴霾的。但在阳光明媚时，你是能看到阳光的，我在这个地方看见过阳光，阳光，阳光，阳光。'
    str2 = '一口下去，香味四溢，香味四溢，讓人回味無窮，讓人回味無窮。這款來自意大利的進口油炸鍋，採用食品級鋁合金材質製作。'
    str3 = '就像是女性的高跟鞋，穿上一双高跟鞋，就像是女性的高跟鞋，穿上一双高跟鞋，就像是女性的高跟鞋。'
    # convertedStr = convert_s2c(to_convert)
    # print(convertedStr)
    # aa=[to_convert]

    # result = chinese_post_processing(data, chinese_search_template)
    # tool_box.write_file(writeFile, result)
    ans = getResult("aaa", "aaa", "aaa bbb", 5, "GPT2")
    # ans = remove_last_sentence(str3)
    # ans = remove_duplicated_sub_sentence(str3)
    # print(ans)
    result = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
    print(ans)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
