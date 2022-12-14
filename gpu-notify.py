#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv(override=True)
import subprocess
import json
import time
import requests
from pynvml.smi import nvidia_smi
import os
WEBHOOK_URL=os.getenv('WEBHOOK_URL')
WAIT = 3600 #1h
SLEEP= 60 #1min
CYCLE = 86400 #24h
start = time.perf_counter()
command = "nvidia-smi pmon -s u -o DT -c 1 | jc --df -p | jq 'map(select(.type==\"C\")) | map(select(.sm==\"-\"))'"
# pidsはpidと時刻の辞書
pids = {}
headers = {
    'Content-Type': 'application/json',
}
if __name__ == '__main__':

    while True:
        output_str =  json.loads(subprocess.run(command,capture_output=True, shell=True).stdout)
        end = time.perf_counter()
        time.sleep(SLEEP)
        if (end-start>CYCLE):
            break
        if (output_str==[]):
            continue
        else:
            for i in output_str:
                if (i["pid"] in pids.keys()):
                    if(pids[i["pid"]][1]==1):
                        continue
                    elif (time.perf_counter()-pids[i["pid"]][0]>WAIT):
                        # おそらくこのコードだと、GPU0(特定GPU)のみになることに注意
                        pysmi = nvidia_smi.getInstance().DeviceQuery()["gpu"][0]["processes"]["pid"==i["pid"]]
                        # pid -> ユーザー名はpsコマンド以外で取得する術を知りませんでした
                        ps = subprocess.run("ps axo user,pid | grep {}".format(i["pid"]),capture_output=True,encoding="utf-8", shell=True).stdout[:-8]
                        # 全然改行してくれない
                        json_data = {
                            'text': 'Hi, {} \npid:{}, {}MiB process remains without computing.\nPlease shutdown your notebook or process.'.format(ps,i["pid"],pysmi["used_memory"]),
                        }
                        response = requests.post(WEBHOOK_URL, headers=headers, json=json_data)
                        pids[i["pid"]]=[time.perf_counter(),1]
                    else:
                        continue
                else:
                    pids[i["pid"]]=[time.perf_counter(),0]
    print(pids)
