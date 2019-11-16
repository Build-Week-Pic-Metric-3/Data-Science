from PicMetric.functions.imgdir import get_pred_data
import json

class Imgdir_Handler:
    def __init__(self, url_list):
        self.url_list = url_list
    
    def get_data(self):
        data = dict()
        for url in self.url_list:
            data[url] = get_pred_data(url)
        return json.dumps(data)
        


        