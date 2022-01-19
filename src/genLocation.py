from unittest import result
import requests
import random
import json

#ランダムな住所を生成する
json_url = 'http://geoapi.heartrails.com/api/json?method=searchByGeoLocation'

# APIリクエスト関数
def get_data(lug,lat):
    payload = {'method': 'searchByGeoLocation', 'x': lug, 'y': lat}
    try:
        ret = requests.get(json_url, params=payload)
        json_ret = ret.json()
    except requests.exceptions.RequestException as e:
        print("ErrorContent: ",e)

    return json_ret

# 住所データの整形関数
def serealize_data(data):
    try:
        dic = data['response']['location'][0]
        det = dic['prefecture'] + dic['city'] + dic['town']
        return det
    except KeyError as e:
        print(e)

# 軽度・緯度に使う乱数の生成
def gene_number(lug_fnum, lug_lnum, lat_fnum, lat_lnum):
    lug = round(random.uniform(lug_fnum,lug_lnum),6)
    lat = round(random.uniform(lat_fnum,lat_lnum),6)
    return lug,lat

def main():
    while(True):
        try:
            lug,lat = gene_number(129,145,30,45)
            ret = get_data(lug,lat)
            if serealize_data(ret) != None:
                result = serealize_data(ret)
                break
        except:
            return "東京都千代田区千代田1-1"
    return result                     