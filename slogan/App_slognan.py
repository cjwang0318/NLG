# conda install flask
from flask import Flask, request
from flask import url_for
from datetime import datetime
import os
import sys
import random

sys.path.append("..")
import tool_box as tb


class web_server:

    def __init__(self):
        # create app
        self.app = Flask(__name__)

        # web api setting
        self.app.add_url_rule('/status', view_func=self.sendStatus, methods=['GET'])
        self.app.add_url_rule('/getResult', view_func=self.getResult, methods=['POST'])
        # self.app.add_url_rule('/image/query', view_func=self.queryImg, methods=['GET'])

        # init slognan dictionary
        self.slognan_dict = self.load_slognan_dict("./slognan_dict/slognan.txt")
        self.slognan_dict_size = len(self.slognan_dict)

        # record status
        self.status = "free"
        self.failCode = ['1', '2', '3', '4', '5']

        # run flask
        self.app.run(host='0.0.0.0', port=5002, threaded=False)

    def sendStatus(self):  # 確認server的狀態
        answer = {"status": self.status}
        return answer

    def load_slognan_dict(self, dict_path):
        slognan_dict = {}
        slognan_list = tb.read_file(dict_path, 0)
        i = 0
        for slognan in slognan_list:
            slognan_dict[i] = slognan
            i = i + 1
        return slognan_dict

    def get_random_index(self, size, n_sample):
        index = random.sample(range(size), n_sample)
        return index

    def log_results(self, keyword, result):
        logList = []
        logFile = "log.txt"
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
        logList.append("----- " + time + " -----\n")
        logList.append("原始關鍵字：" + keyword + "\n")
        for id, sample in enumerate(result):
            logList.append("文案" + str(id) + ":\t" + sample + "\n")
        tb.append_file(logFile, logList)

    def getResult(self):  # 呼叫文案生成API
        # change status
        self.status = "processing"

        # decode json
        content = request.json
        keyword = content['keyword']
        # nsamples = content['nsamples']
        nsamples = 20
        index_list = self.get_random_index(self.slognan_dict_size, nsamples)
        # print(index_list)
        results = []
        for index in index_list:
            slogan = self.slognan_dict.get(index)
            slogan = slogan.replace("@%@", keyword)
            # print(slogan)
            results.append(slogan)

        answer = {"keyword": keyword, "nsamples": str(nsamples), "samples": results}
        self.log_results(keyword, results)
        # change status
        self.status = "free"
        return answer


if __name__ == '__main__':
    wbs = web_server()
