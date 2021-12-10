import pandas as pd
import tool_box

if __name__ == '__main__':
    dataPath = "./Tao/data/"
    readFile = "content_tag_dataset.txt"
    #readFile = "test.txt"
    writeFile = "results.txt"
    top_n_tags = 5
    lines = tool_box.read_file(dataPath + readFile, 0)
    resultList = []
    lineCount = 1
    for line in lines:
        print(repr(lineCount)+":"+line)
        elements = line.split("\t")
        if len(elements) !=2:
            lineCount = lineCount + 1
            continue
        description = elements[0]
        tags = elements[1]
        tagSet = tags.split(";")
        dict = {}
        for tag in tagSet:
            nameValueSet = tag.split(":")
            tagName = nameValueSet[0]
            tagValue = format(float(nameValueSet[1]), '.4f')
            dict.update({tagName: float(tagValue)})
        df = pd.DataFrame(list(dict.items()), columns=['tagName', 'tagValue'])
        df_sorted = df.sort_values(by="tagValue", ascending=False).head(top_n_tags)
        # print(df_sorted)
        str = description + "\t"
        i = 1
        for index, row in df_sorted.iterrows():
            if i < 5:
                str = str + row['tagName'] + "\t" + repr(row['tagValue']) + "\t"
            else:
                str = str + row['tagName'] + "\t" + repr(row['tagValue'])
            i = i + 1
        resultList.append(str + "\n")
        lineCount = lineCount + 1
    tool_box.write_file(dataPath + writeFile, resultList)
