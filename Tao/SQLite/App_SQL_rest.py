from flask import Flask, request
import sqlite3
import sql_search as ss
import SQLite_args as args
import NLG_client as nc
import sys

sys.path.append("..")
import dictionary_search as ds


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

        # init description dictionary search
        self.description_generation_threshold = args.description_generation_threshold
        self.description_path = args.description_path
        self.dict = ds.load_data(self.description_path)

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
        category = content['category']
        # 通用類型 = 1
        # 服飾類型 = 2
        nsamples = args.nsamples
        nkeywords = args.nkeywords

        search_type = args.search_type
        # description dictionary search check 優良文案字典查詢
        flag = ds.dictionary_search_check(keyword, self.dict, self.description_generation_threshold)
        # print("flag="+str(flag))
        if flag:
            # 使用優良文案回傳
            generate_type = "DICT"
            answer = ds.dictionary_search_rest(self.dict, keyword, keyword, keyword, nsamples, generate_type)
        else:
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
                    ss.log_results(keyword, seg_keywords, sql_search_keyword, results, generate_type, category)
            elif (search_type == 'seg_search'):
                seg_keywords, keyword_list = ss.generate_candidate_keyword_list(keyword)
                sql_search_keyword, results = ss.get_seg_result(self.cursor, keyword_list, nsamples)
                if results == None:
                    answer = {"keyword": str(keyword), "nsamples": str(nsamples), "samples": ["對不起～此關鍵字無相關文案可推薦"]}
                else:
                    generate_type = "seg_search"
                    answer = {"keyword": str(sql_search_keyword), "nsamples": str(nsamples), "samples": results}
                    ss.log_results(keyword, seg_keywords, sql_search_keyword, results, generate_type, category)
            elif (search_type == 'key_search'):
                seg_keywords, keyword_SQLquery_list = ss.generate_candidate_query_list(keyword, nkeywords)
                sql_search_keyword, results = ss.get_keyword_result(self.cursor, keyword_SQLquery_list, nsamples)
                if results == None:
                    answer = {"keyword": str(keyword), "nsamples": str(nsamples), "samples": ["對不起～此關鍵字無相關文案可推薦"]}
                else:
                    generate_type = "key_search"
                    answer = {"keyword": str(sql_search_keyword), "nsamples": str(nsamples), "samples": results}
                    ss.log_results(keyword, seg_keywords, sql_search_keyword, results, generate_type, category)
            else:
                answer = {"keyword": str(keyword), "nsamples": str(nsamples), "samples": ["對不起～系統發生錯誤"]}
            # 如果SQL搜尋沒有找到文案，是否使用NLG模式生成文案
            # results = None
            if (args.NLG_operation and results == None):
                # 如果使用NLG模型，進入系統使用關鍵字為關鍵詞擷取後的結果，不是原本的完整的查詢詞
                item_split = keyword_SQLquery_list[0].split("\t")
                nlg_keyword = item_split[0]
                answer = nc.call_nlg(nlg_keyword)

        # change status
        self.status = "free"
        return answer


if __name__ == '__main__':
    wbs = web_server()
