# conda install flask
# 必需搭配 App_rest.py(Rest服務執行檔), generate_rest.py(文案生成), args.py(參數設定檔)
from flask import Flask, request
from flask import url_for
from opencc import OpenCC
import os
import PostProcessing
import args
import generate_rest as gs
import tool_box as tb
import client_send as cs
from transformers import GPT2LMHeadModel


class web_server:

    def __init__(self):
        # create app
        self.app = Flask(__name__)

        # web api setting
        self.app.add_url_rule('/status', view_func=self.sendStatus, methods=['GET'])
        self.app.add_url_rule('/getResult', view_func=self.getResult, methods=['POST'])
        # self.app.add_url_rule('/image/query', view_func=self.queryImg, methods=['GET'])

        # init core
        if args.segment:
            from tokenizations import tokenization_bert_WMGeg as tokenization_bert
        else:
            from tokenizations import tokenization_bert
        self.tokenizer = tokenization_bert.BertTokenizer(vocab_file=args.tokenizer_path)
        self.model = GPT2LMHeadModel.from_pretrained(args.model_path)

        # init vocab list for checking word is [NUK] or not?
        self.vocabList = tb.read_file(args.tokenizer_path, 0)

        # record status
        self.status = "free"
        self.failCode = ['1', '2', '3', '4', '5']

        # run flask
        self.app.run(host='0.0.0.0', port=5000, threaded=False)

    def sendStatus(self):  # 確認server的狀態
        answer = {"status": self.status}
        return answer

    def convert_tw2s(self, str):
        cc = OpenCC('tw2sp')  # convert from Simplified Chinese to Traditional Chinese
        converted = cc.convert(str)
        return converted

    def oov_checking(self, seg_keywords, vocabList):
        seg_keyword_without_oov = ""
        keywordList = seg_keywords.split(" ")
        for word in keywordList:
            if word in vocabList:
                seg_keyword_without_oov = seg_keyword_without_oov + word + " "
        seg_keyword_without_oov = seg_keyword_without_oov.strip()
        return seg_keyword_without_oov

    def getResult(self):  # 呼叫文案生成API
        # change status
        self.status = "processing"

        # generate model type
        generate_type="GPT2"

        # decode json
        content = request.json
        keyword = content['keyword']
        nsamples = args.nsamples

        #tranform to lowcase
        keyword=keyword.lower()

        # call segmentation
        #print("keyword="+keyword)
        seg_keywords = cs.call_CKIP(keyword)
        #print("CKIP="+seg_keywords)

        # translate to simple Chinese(List to String)
        seg_keywords_simple = self.convert_tw2s(seg_keywords)
        #print("simple Chinese=" + keyword)

        # OOV checking
        seg_keyword_without_oov = self.oov_checking(seg_keywords_simple, self.vocabList)
        #answer = {"keyword": seg_keyword_without_oov}
        # call generator
        # cmd = 'python ./generate.py --device=0 --length=30 --temperature=0.3 --topk=20 --nsamples='+str(nsamples)+' --prefix='+str(keyword)+' --fast_pattern --save_samples --save_samples_path=./output'
        # print(cmd)
        # os.system(cmd)
        #print("seg_keyword_without_oov="+seg_keyword_without_oov)

        if seg_keyword_without_oov =="":
            answer = {"keyword": str(keyword), "nsamples": str(nsamples),"samples":["對不起～此關鍵字無相關可推薦文案"]}
        else:
            gs.generator_rest(seg_keyword_without_oov, self.model, self.tokenizer)
            # call postProcessing
            seg_keyword_without_oov=seg_keyword_without_oov.replace(" ","")
            #print("seg_keyword_without_oov_whitespace=" + seg_keyword_without_oov)
            answer=PostProcessing.getResult(keyword, seg_keywords, seg_keyword_without_oov, nsamples, generate_type)

        # change status
        self.status = "free"
        return answer


if __name__ == '__main__':
    wbs = web_server()
