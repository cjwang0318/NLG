import tool_box as tb

dict=[]
#dataset=tb.read_file("./vocab_clothes_normalized.txt",0)
dataset=tb.read_file("./vocab_desc_only_top100k.txt",0)
for line in dataset:
    if len(line)<2:
        continue
    else:
       dict.append(line+",1\n")
tb.write_file("./dict.csv",dict)