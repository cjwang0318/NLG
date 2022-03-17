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
    start = time.time()
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
    end = time.time()
    print('time: ', end - start)
    return seg_query


if __name__ == '__main__':
    keyword = "時尚風公主裙"
    call_CKIP(keyword)
