import os
import json
import gzip
import pandas as pd

import tool_box

if __name__ == '__main__':
    dataPath = "./Amazon/data/"
    readFile = "meta_Arts_Crafts_and_Sewing.json.gz"
    writeFile = "results.json"
    data = []
    with gzip.open(dataPath + readFile) as f:
        for l in f:
            data.append(json.loads(l.strip()))

    # total length of list, this number equals total number of products
    # print(len(data))

    # first row of the list
    # print(data[0])

    # convert list into pandas dataframe
    df = pd.DataFrame.from_dict(data)
    # print(df)
    # df3 = df.fillna('')
    # df4 = df3[df3.title.str.contains('getTime')]  # unformatted rows
    # print(len(df4))

    # print(df.iloc[0])
    # print("description= "+str(df.at[1,"description"]))
    # print("description= " + str(df.at[3, "description"]))
    # print("description= " + str(df.at[18, "description"]))
    totalNum = len(df)
    count = 0
    charList = "[]"
    with open(dataPath + writeFile, "w", encoding='utf-8') as f:
        f.write("[")
        for i in range(len(df)):
            # print("description= " + str(df.at[i, "description"]))
            #print(i)
            line = str(df.at[i, "description"])

            if "</" in line or "[]" in line:
                continue
            else:
                line = line.replace("<br>", "")
                line = tool_box.remove_chars_in_sentence(charList, line)
                line = line[1:len(line) - 1]
                line = line.replace("\"", "")
                line = line.replace("\\", "")
                # print(line)
                count = count + 1
                if i < len(df)-1:
                    f.write("\"" + line + "\", ")
                else:
                    f.write("\"" + line + "\"")
        f.write("]")
    reservationRate = round(count / totalNum, 4)
    print("Reservation Rate=" + str(reservationRate) + "(" + str(count) + "/" + str(totalNum) + ")")

