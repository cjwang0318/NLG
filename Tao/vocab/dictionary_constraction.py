import tool_box as tb


def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def dictionary_generation(path):
    dict = []
    dataset = tb.read_file(path, 0)
    for line in dataset:
        if len(line) < 2:  # 判斷長度
            continue
        elif (isEnglish(line)):  # 判斷是否為英文
            continue
        else:
            # line=convert_s2c(line)
            dict.append(line + ",1\n")
    tb.write_file("./dict.csv", dict)


if __name__ == '__main__':
    #path = "./vocab_desc_only_top100k.txt"
    path = "./productName.txt"
    dictionary_generation(path)

    # keyword1 = "[SEP]"
    # keyword2 = "裝aa"
    # keyword3 = "abc"
    # print(isEnglish(keyword1))
    # print(isEnglish(keyword2))
    # print(isEnglish(keyword3))
