import requests
#import time
import SQLite_args as args
import json

def call_nlg(query):
    sendMessage_query = {
        "keyword": query,
        "nsamples": args.nsamples
    }
    #start = time.time()
    # sent json to server
    res = requests.post('http://localhost:5000/getResult', json=sendMessage_query)
    if res.ok:
        outputs = res.json()
        #print(outputs)
        print("Call NLG Engine!")

    #end = time.time()
    #print('time: ', end - start)
    return outputs