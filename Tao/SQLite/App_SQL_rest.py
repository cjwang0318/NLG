from flask import Flask, request
import sqlite3
import sql_search as ss


class web_server:

    def __init__(self):
        # create app
        self.app = Flask(__name__)

        # web api setting
        self.app.add_url_rule('/status', view_func=self.sendStatus, methods=['GET'])
        self.app.add_url_rule('/getResult', view_func=self.getResult, methods=['POST'])
        # self.app.add_url_rule('/image/query', view_func=self.queryImg, methods=['GET'])

        # init sqlite core
        self.db = sqlite3.connect('./tao_test.db')
        self.cursor = self.db.cursor()

        # record status
        self.status = "free"
        self.failCode = ['1', '2', '3', '4', '5']

        # run flask
        self.app.run(host='0.0.0.0', port=5001, threaded=False)

    def sendStatus(self):  # 確認server的狀態
        answer = {"status": self.status}
        return answer

    def getResult(self):  # 呼叫文案生成API
        # change status
        self.status = "processing"

        # decode json
        content = request.json
        keyword = content['keyword']
        nsamples = 5

        results = ss.get_result(self.cursor, keyword, nsamples)

        if results == None:
            answer = {"keyword": str(keyword), "nsamples": str(nsamples), "samples": ["對不起～此關鍵字無相關文案可推薦"]}
        else:
            # generate model type
            generate_type = "SQL"
            seg_keywords = keyword
            keyword_without_oov = keyword
            answer = ss.log_results(keyword, seg_keywords, keyword_without_oov, results, generate_type)
        # change status
        self.status = "free"
        return answer


if __name__ == '__main__':
    wbs = web_server()
