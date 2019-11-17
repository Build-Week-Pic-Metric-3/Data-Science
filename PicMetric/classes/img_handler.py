from PicMetric.functions.img import get_pred_data
import json

class Img_Handler:
    def __init__(self, url_list):
        self.url_list = url_list
    
    def get_data(self, func):
        data = dict()
        for url in self.url_list:
            data[url] = get_pred_data(url, func)
        return data
        


        