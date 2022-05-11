import tool_box as tb


def load_data():
    dictionary_path = "./dict/dictionary.txt"
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


if __name__ == '__main__':
    aa = load_data()
    print(aa)
