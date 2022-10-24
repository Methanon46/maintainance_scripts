#!/usr/bin/env python3
import subprocess
import json
import time
import requests
from pynvml.smi import nvidia_smi

WEBHOOK_URL="https://husm.webhook.office.com/webhookb2/62c2a56f-c97c-4fcf-8945-0ac06273c91d@16fbddaa-9f9a-42a5-afbf-d65e420db2fc/IncomingWebhook/f371a2f21034457e8437556e263dde7a/c6f83a96-8b44-4847-985f-33756fd87a73"
WAIT = 3600
CYCLE = 86400
start = time.perf_counter()
command = "nvidia-smi pmon -s u -o DT -c 1 | jc --df -p | jq 'map(select(.type==\"C\")) | map(select(.sm==\"-\"))'"
command_byte = command.encode()
pids = {}
headers = {
    'Content-Type': 'application/json',
}
if __name__ == '__main__':

    while True:
        output_str =  json.loads(subprocess.run(command,capture_output=True, shell=True).stdout)
        end = time.perf_counter()
        # if (end - start > 86400):
        #     break
        time.sleep(60)
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
                        pysmi = nvidia_smi.getInstance().DeviceQuery()["gpu"][0]["processes"]["pid"==i["pid"]]
                        json_data = {
                            'text': 'pid:{}, {}MiB process remains without computing.\nPlease shutdown your notebook or process.'.format(i["pid"],pysmi["used_memory"]),
                        }
                        response = requests.post(WEBHOOK_URL, headers=headers, json=json_data)
                        pids[i["pid"]]=[time.perf_counter(),1]
                    else:
                        continue
                else:
                    pids[i["pid"]]=[time.perf_counter(),0]
    print(pids)
