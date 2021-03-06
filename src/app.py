import os
import configparser
import time
import threading
import pandas
import markovify
import requests
import getdata
import exportModel
import genLocation

# コンフィグの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini', encoding='utf-8')
elements = ['serihu', 'joukyou']



def genModel(elements):
    date_index = pandas.date_range(start="2018-01", end="2022-01", freq="M").to_series().dt.strftime("%Y%m")
    for i in elements:
        path = 'chainfiles/' + i + '.json'
        size = 2 if i == 'iti' else 3
        list = getdata.getData(i, date_index)
        exportModel.generateAndExport(list, path, size)


def genText(elements):
    result = []
    for i in elements:
        path = 'chainfiles/' + i + '.json'
        with open(path) as f:
            textModel = markovify.Text.from_json(f.read())
            sentence = textModel.make_sentence(tries=500)
            if i == 'serihu':
                sentence = '「' + sentence + '」'
            result.append(sentence)
    return result


def post_toot(domain, access_token, params):
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    url = "https://{}/api/v1/statuses".format(domain)
    response = requests.post(url, headers=headers, json=params)
    if response.status_code != 200:
        raise Exception('リクエストに失敗しました。')
    return response

def worker():
    # モデルの作成について
    print("開始します…")
    if (os.path.isfile('chainfiles/serihu.json')):
        print("モデルは再生成されません")
    else:
        genModel(elements)
    domain = config_ini['read']['domain']
    write_access_token = config_ini['write']['access_token']
    result = genText(elements)
    sentence = result[0] + '\n' + result[1]
    location = genLocation.main()
    sentence = sentence.replace(' ', '') + "\n" + location + 'にて #bot'
    try:
        post_toot(domain, write_access_token, {"status": sentence})
        print("投稿しました。 内容: " + sentence)
    except Exception as e:
        print("投稿エラー: {}".format(e))

def schedule(f, interval=1200, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)

if __name__ == "__main__":
    # 定期実行部分
    schedule(worker)