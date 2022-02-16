#conda install flask
#必需搭配 App_rest.py(Rest服務執行檔), generate_rest.py(文案生成), args.py(參數設定檔)
from flask import Flask, request
from flask import url_for
from opencc import OpenCC
import os
import PostProcessing
import args
import generate_rest as gs
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
            from tokenizations import tokenization_bert_word_level as tokenization_bert
        else:
            from tokenizations import tokenization_bert
        self.tokenizer = tokenization_bert.BertTokenizer(vocab_file=args.tokenizer_path)
        self.model = GPT2LMHeadModel.from_pretrained(args.model_path)

        # record status
        self.status = "free"
        self.failCode = ['1', '2', '3', '4', '5']

        # run flask
        self.app.run(host='0.0.0.0', port=5000, threaded=False)

    def sendStatus(self):  # 確認server的狀態
        answer = {"status": self.status}
        return answer

    def convert_tw2s(self, str):
        cc = OpenCC('tw2s')  # convert from Simplified Chinese to Traditional Chinese
        converted = cc.convert(str)
        return converted

    def getResult(self):  # 呼叫文案生成API
        # change status
        self.status = "processing"

        # decode json
        content = request.json
        keyword = content['keyword']
        #nsamples = content['nsamples']
        nsamples=args.nsamples
        keyword = self.convert_tw2s(keyword)
        # call generator
        #cmd = 'python ./generate.py --device=0 --length=30 --temperature=0.3 --topk=20 --nsamples='+str(nsamples)+' --prefix='+str(keyword)+' --fast_pattern --save_samples --save_samples_path=./output'
        #print(cmd)
        #os.system(cmd)
        gs.generator_rest(keyword, self.model, self.tokenizer)
        # call postProcessing
        answer=PostProcessing.getResult(keyword, nsamples)

        # change status
        self.status = "free"
        return answer

if __name__ == '__main__':
    wbs = web_server()
