from flask import Flask, request
import sqlite3
import sql_search as ss
import SQLite_args as args


class web_server:

    def __init__(self):
        # create app
        self.app = Flask(__name__)

        # web api setting
        self.app.add_url_rule('/status', view_func=self.sendStatus, methods=['GET'])
        self.app.add_url_rule('/getResult', view_func=self.getResult, methods=['POST'])
        # self.app.add_url_rule('/image/query', view_func=self.queryImg, methods=['GET'])

        # init sqlite core
        self.db = sqlite3.connect(args.database)
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
        nsamples = args.nsamples

        search_type = args.search_type
        if (search_type == 'exactly_search'):
            results = ss.get_result(self.cursor, keyword, nsamples)
            if results == None:
                answer = {"keyword": str(keyword), "nsamples": str(nsamples), "samples": ["對不起～此關鍵字無相關文案可推薦"]}
            else:
                # generate model type
                generate_type = "exactly_search"
                seg_keywords = keyword
                sql_search_keyword = keyword
                answer = {"keyword": str(sql_search_keyword), "nsamples": str(nsamples), "samples": results}
                ss.log_results(keyword, seg_keywords, sql_search_keyword, results, generate_type)
        elif (search_type == 'seg_search'):
            seg_keywords, keyword_list = ss.generate_candidate_keyword_list(keyword)
            sql_search_keyword, results = ss.get_seg_result(self.cursor, keyword_list, nsamples)
            if results == None:
                answer = {"keyword": str(keyword), "nsamples": str(nsamples), "samples": ["對不起～此關鍵字無相關文案可推薦"]}
            else:
                generate_type = "seg_search"
                answer = {"keyword": str(sql_search_keyword), "nsamples": str(nsamples), "samples": results}
                ss.log_results(keyword, seg_keywords, sql_search_keyword, results, generate_type)
        else:
            answer = {"keyword": str(keyword), "nsamples": str(nsamples), "samples": ["對不起～系統發生錯誤"]}
        # change status
        self.status = "free"
        return answer


if __name__ == '__main__':
    wbs = web_server()
