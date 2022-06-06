import requests
import time
import SQLite_args as args
import json


def call_CKIP(query):
    sendMessage_query = {
        "sentences": [query],
        "dictionary": args.dictionary
    }
    sendMessage_json = json.dumps(sendMessage_query)
    # start = time.time()
    # sent json to server
    res = requests.post('http://' + args.segmentation_server_IP + '/getResult', json=sendMessage_json)
    seg_query = ""
    if res.ok:
        outputs = res.json()
        # print(outputs)
        for word in outputs[0]:
            seg_query = seg_query + " " + word
    else:
        print("Abnormal return, please check CKIP")
    seg_query = seg_query.strip()
    # print(seg_query)
    # end = time.time()
    # print('time: ', end - start)
    return seg_query


def call_keyword_extraction(query):
    # query = {"sentence": "寶寶 次氯酸 水 - 微 酸性 家庭 OK 組 ( 次氯酸 水 衛生 居家 防疫 婦幼 )", "topn":5}
    sendMessage_query = {
        "sentence": query,
        "topn": args.nkeywords
    }
    sendMessage_json = json.dumps(sendMessage_query)
    # print(sendMessage_json)
    # start = time.time()
    # sent json to server
    res = requests.post('http://' + args.keyword_extraction_server_IP + '/getResult', json=sendMessage_json)
    if res.ok:
        outputs = res.json()
        # for line in outputs:
        #    print(line)
    else:
        print("Abnormal return, please check keyword extraction service")
    # end = time.time()
    # print('time: ', end - start)
    return outputs
