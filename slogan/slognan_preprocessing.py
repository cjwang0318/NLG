from os import walk
from os.path import join
import sys

sys.path.append("..")
import tool_box as tb


def get_fileName_and_filePath(mypath):
    # 遞迴列出所有檔案的絕對路徑
    dict = {}
    for root, dirs, files in walk(mypath):
        for f in files:
            fullpath = join(root, f)
            # print(fullpath)
            fileName = f.replace(".txt", "")
            dict[fileName] = fullpath
    return dict


if __name__ == '__main__':
    # 指定要列出所有檔案的目錄
    datalist = []
    slognan_set = set()
    mypath = "./data"
    dict = get_fileName_and_filePath(mypath)
    for key, value in dict.items():
        lines = tb.read_file(value, 0)
        line_num = 1
        for line in lines:
            slognan_template = line.replace(key, "@%@")
            if "@%@" not in slognan_template:
                print("please have a check on:" + key + ".txt")
                print("line_num=" + str(line_num) + ", string=" + slognan_template)
                # exit()
            slognan_set.add(slognan_template + "\n")
            line_num = line_num + 1
    datalist = list(slognan_set)
    tb.write_file("./slognan.txt", datalist)
