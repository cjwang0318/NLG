import tool_box as tb

dataPath = "E:/item_desc_dataset.txt"
writePath = "E:/item_desc_dataset.seg.txt"
lines = tb.read_file(dataPath, 0)
item = []
for line in lines:
    strList = line.split("\t")
    item.append(strList[1]+"\n")
tb.write_file(writePath, item)
