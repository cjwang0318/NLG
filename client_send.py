# conda install requests
import requests
import time
import args
import json


def call_CKIP(query):
    sendMessage_query = {
        "sentences": [query],
        "dictionary": args.dictionary
    }
    sendMessage_json = json.dumps(sendMessage_query)
    #start = time.time()
    # sent json to server
    res = requests.post('http://' + args.segmentation_server_IP + '/getResult', json=sendMessage_json)
    seg_query = ""
    if res.ok:
        outputs = res.json()
        #print(outputs)
        for word in outputs[0]:
            seg_query = seg_query + " " + word
    seg_query = seg_query.strip()
    #print(seg_query)
    #end = time.time()
    #print('time: ', end - start)
    return seg_query

def call_nlg(query):
    sendMessage_query = {
        "keyword": query,
        "nsamples": args.nsamples
    }
    start = time.time()
    # sent json to server
    res = requests.post('http://192.168.50.32:5001/getResult', json=sendMessage_query)
    if res.ok:
        outputs = res.json()
        print(outputs)

    end = time.time()
    print('time: ', end - start)
    return outputs


if __name__ == '__main__':
    keyword = "超級無敵馬甲西裝"
    keyword = "A Beauty Girl 性感鋼圈美背成套內衣(開運紅,共2套)"
    keyword = "樂活e棧-聖誕節MIT豪華加厚禦寒版-聖誕老人服裝(豪華5件套組)"
    #keyword = "逼逼逼逼"
    # seg_query=call_CKIP(keyword)
    # print(seg_query)
    call_nlg(keyword)
