import pandas as pd
import tool_box

if __name__ == '__main__':
    dataPath = "./Amazon/data/"
    #readFile = "content_tag_sample.txt"
    readFile = "test.txt"
    writeFile = "results.json"
    lines=tool_box.read_file(dataPath + readFile,0)
    for line in lines:
        elements=line.split("\t")
        description=elements[0]
        tags=elements[1]
        tagSet=tags.split(";")
        dict={}
        for tag in tagSet:
            nameValueSet=tag.split(":")
            tagName=nameValueSet[0]
            tagValue=format(float(nameValueSet[1]), '.4f')
            dict.update({tagName:float(tagValue)})
        df=pd.DataFrame(list(dict.items()),columns=['tagName', 'tagValue'])
        df_sorted=df.sort_values(by="tagValue", ascending=False).head(5)
        #print(df)
        print(df_sorted.values.tolist())
