# install opencc
# pip install opencc-python-reimplemented
from opencc import OpenCC
import tool_box
import re


def convert_s2c(str):
    cc = OpenCC('s2tw')  # convert from Simplified Chinese to Traditional Chinese
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


def chinese_post_processing(dataList):
    result = []
    for line in dataList:
        convertedLine = convert_s2c(line)
        chineseCheck = tool_box.check_contain_chinese(convertedLine)
        if "==========================================================================================" in convertedLine:
            result.append(convertedLine+"\n\n")
        elif "========================================" in convertedLine:
            result.append(convertedLine+"\n")
        elif chineseCheck == None:
            continue
        else:
            index = chinese_sentence_search(chinese_search_template, convertedLine)
            cut_sentence = convertedLine[:index] + "。\n"
            result.append(cut_sentence)
            print(cut_sentence)
    return result


if __name__ == '__main__':
    chinese_search_template = '，。！'
    dataPath = "./output/"
    readFile = "samples.txt"
    writeFile = "results.txt"
    data = tool_box.read_file(dataPath + readFile, 0)
    to_convert = '天空是有些阴霾的。但在阳光明媚时，你是能看到阳光的。我在这个地方看见过阳光。阳光'
    # convertedStr = convert_s2c(to_convert)
    # print(convertedStr)
    # aa=[to_convert]
    result = chinese_post_processing(data)
    tool_box.write_file(writeFile, result)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
