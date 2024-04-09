import requests as rq
import json
import os

def send_post(url,graphdata):
    if graphdata is None:
        return

    if url is None:
        print("url is None")
        return
    headers = {'Content-Type': 'application/json'}  # 设置请求头
    # backData = rq.post(url, data=json.dumps(graphdata), headers=headers)  # 发送POST请求，同时设置请求头
    backData = rq.post(url, data=graphdata, headers=headers)  # 发送POST请求，同时设置请求头
    if backData and backData.status_code == 200:
        print('数据已发送')
    else:
        print('数据发送失败')

# 示例调用
# send_post('http://0.0.0.0:8099/send/json/', {'data': 123})