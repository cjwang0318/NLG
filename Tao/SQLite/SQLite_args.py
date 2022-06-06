# exactly_search &  key_search使用沒斷詞的資料庫
database = './tao_cht.db'
# seg_search 使用 斷詞後的資料庫
# database = './tao_seg_cht.db'
nsamples = 5
'''
exactly_search：搜尋必需完全包含全部關鍵字
seg_search：搜尋前先斷詞，例如：AA BB CC，先完全比對(AA BB CC)，依序縮減(BB CC)，最後(CC)
key_search：搜尋前先斷詞，再做關鍵字擷取(AA BB CC, 順序根據演算法所提供的權重)，擷取幾個關鍵字根據nkeywords的設定，然後再使用模糊搜尋`itemName` LIKE '%AA%' AND `itemName` LIKE '%BB%'，
            若沒有就縮短為 itemName` LIKE '%AA%' 
'''
# search_type='exactly_search'
# search_type = 'seg_search'
search_type = 'key_search'
segmentation_server_IP = "192.168.50.29:5000"
keyword_extraction_server_IP = "192.168.50.29:5001"
nkeywords = 3
dictionary = "tao_top100K"
NLG_operation = True
