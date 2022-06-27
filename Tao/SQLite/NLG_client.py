import requests
# import time
import SQLite_args as args
import json


def call_nlg(query):
    sendMessage_query = {
        "keyword": query,
        "nsamples": args.nsamples
    }
    # start = time.time()
    # sent json to server
    res = requests.post('http://localhost:5000/getResult', json=sendMessage_query)
    if res.ok:
        outputs = res.json()
        # print(outputs)
        print("Call NLG Engine!")

    # end = time.time()
    # print('time: ', end - start)
    return outputs


def call_nlg_num_sample(query, num_sample):
    sendMessage_query = {
        "keyword": query,
        "nsamples": num_sample
    }
    # start = time.time()
    # sent json to server
    res = requests.post('http://localhost:5000/getResult', json=sendMessage_query)
    # res = requests.post('http://192.168.50.32:5000/getResult', json=sendMessage_query)
    if res.ok:
        outputs = res.json()
        results = outputs['samples']
        # print(results)
        # print(type(results))
    # end = time.time()
    # print('time: ', end - start)
    return results


if __name__ == '__main__':
    keyword = "及膝裙 牛仔"
    result = call_nlg_num_sample(keyword, 3)
    print(result)
