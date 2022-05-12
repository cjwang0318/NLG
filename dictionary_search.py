import random
import dictionary_load
import args

nsamples = args.nsamples
threshold = 0.01


def in_dictionary(keyword, dict):
    if keyword in dict:
        return True
    else:
        return False


def list_shuffle(list):
    random.shuffle(list)
    return list


def list_fetch_top_K(list, top_k):
    length = len(list)
    if length < top_k:
        return list
    else:
        return list[:top_k]


"""
1. 判斷關鍵字是否有在字典檔
2. 若無：呼叫GPT2模組自動生成文案
3. 如果在字典檔，亂數產生一個機率值
4. 如機率於大於某個門檻，就直接使用文案庫中的文案，反之就呼叫GPT2模組自動生成文案
5. 整理文案庫
"""
if __name__ == '__main__':
    dict = dictionary_load.load_data()
    flag = in_dictionary("測試1", dict)
    keyword="測試1"
    dict_prob = random.random()
    if flag is True and dict_prob > threshold:
        list = dict.get(keyword)
        list_shuffle(list)
        list=list_fetch_top_K(list,nsamples)
        #print("flag=" + str(flag))
        answer = {"keyword": str(keyword), "nsamples": str(nsamples), "samples": list}
        print(answer)
    else:
        print("flag=" + str(flag))
        print("call GPT")

    # random.shuffle(list)
