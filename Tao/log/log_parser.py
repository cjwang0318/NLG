import tool_box as tb

if __name__ == '__main__':
    log = []
    path = "./log.txt"
    dataset = tb.read_file(path, 0)
    for line in dataset:
        if "----- " in line:
            keyword = ""
            type = ""
        if "進入生成系統關鍵字：" in line:
            temp = line.split("：")
            keyword = temp[1]
            continue
        if "生成模型類別：" in line:
            temp = line.split("：")
            type = temp[1]
            continue
        if type == "GPT2":
            temp = line.split("\t")
            #print(line)
            if len(temp) == 2:
                log.append(keyword + "\t" + temp[1] + "\n")
            continue

    tb.write_file("./log_parsed.txt", log)
