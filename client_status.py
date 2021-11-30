import requests
import time

start = time.time()

# sent json to server
#res = requests.get('http://192.168.0.3:5000/status')
res = requests.get('http://192.168.100.122:5000/status')
if res.ok:
    data = res.json()
    status = data["status"]
    print(status)

end = time.time()

print('time: ',end-start)