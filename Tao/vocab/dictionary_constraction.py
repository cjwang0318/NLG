import tool_box as tb
from opencc import OpenCC

def convert_s2c(str):
    cc = OpenCC('s2tw')  # convert from Simplified Chinese to Traditional Chinese
    converted = cc.convert(str)
    return converted

dict=[]
#dataset=tb.read_file("./vocab_clothes_normalized.txt",0)
dataset=tb.read_file("./vocab_desc_only_normalized.txt",0)
for line in dataset:
    if len(line)<2:
        continue
    else:
        #line=convert_s2c(line)
        dict.append(line+",1\n")
tb.write_file("./dict.csv",dict)