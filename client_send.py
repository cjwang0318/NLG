# conda install requests
import requests
import time
from opencc import OpenCC

keyword = "傳統色紙"
nsamples = 8

sendMessage_json = {
    "keyword": keyword,
    "nsamples": nsamples
}

start = time.time()
# sent json to server
#res = requests.post('http://192.168.0.3:5000/getResult', json=sendMessage_json)
res = requests.post('http://192.168.100.122:5000/getResult', json=sendMessage_json)
if res.ok:
    outputs = res.json()
    print(outputs)

end = time.time()
print('time: ', end - start)
