import time
import random
import json
from TikTokApi import TikTokApi

api = TikTokApi.get_instance()
# If playwright doesn't work for you try to use selenium
# api = TikTokApi.get_instance(use_selenium=True, executablePath='/usr/bin/firefox')

results = 10
proxies = ['VgR6Xh:tniX7wgDEk@194.32.237.89:1050',
           'VgR6Xh:tniX7wgDEk@45.139.177.168:1050',
           'VgR6Xh:tniX7wgDEk@109.248.205.215:1050',
           'VgR6Xh:tniX7wgDEk@45.84.177.217:1050',
           'VgR6Xh:tniX7wgDEk@45.147.192.88:1050',
           'VgR6Xh:tniX7wgDEk@84.54.53.165:1050',
           'VgR6Xh:tniX7wgDEk@45.140.52.153:1050',
           'VgR6Xh:tniX7wgDEk@188.130.188.145:1050',
           'VgR6Xh:tniX7wgDEk@109.248.48.215:1050',
           'VgR6Xh:tniX7wgDEk@45.90.196.148:1050',
           'VgR6Xh:tniX7wgDEk@45.145.119.56:1050',
           'VgR6Xh:tniX7wgDEk@77.94.1.40:1050',
           'VgR6Xh:tniX7wgDEk@46.8.212.5:1050',
           'VgR6Xh:tniX7wgDEk@45.144.36.146:1050',
           'VgR6Xh:tniX7wgDEk@194.32.237.140:1050',
           'VgR6Xh:tniX7wgDEk@194.156.97.37:1050',
           'VgR6Xh:tniX7wgDEk@45.87.253.105:1050',
           'VgR6Xh:tniX7wgDEk@46.8.15.228:1050',
           'VgR6Xh:tniX7wgDEk@95.182.127.193:1050',
           'VgR6Xh:tniX7wgDEk@46.8.213.56:1050',
           'VgR6Xh:tniX7wgDEk@109.248.204.121:1050',
           'VgR6Xh:tniX7wgDEk@45.139.177.226:1050',
           'VgR6Xh:tniX7wgDEk@45.15.237.224:1050',
           'VgR6Xh:tniX7wgDEk@45.134.183.196:1050',
           'VgR6Xh:tniX7wgDEk@46.8.111.83:1050',
           'VgR6Xh:tniX7wgDEk@46.8.107.229:1050',
           'VgR6Xh:tniX7wgDEk@46.8.10.174:1050',
           'VgR6Xh:tniX7wgDEk@188.130.187.57:1050',
           'VgR6Xh:tniX7wgDEk@95.182.125.17:1050',
           'VgR6Xh:tniX7wgDEk@109.248.13.9:1050',
           'VgR6Xh:tniX7wgDEk@46.8.11.169:1050',
           'VgR6Xh:tniX7wgDEk@185.181.247.24:1050',
           'VgR6Xh:tniX7wgDEk@109.248.166.128:1050',
           'VgR6Xh:tniX7wgDEk@194.156.92.161:1050',
           'VgR6Xh:tniX7wgDEk@46.8.56.23:1050',
           'VgR6Xh:tniX7wgDEk@212.115.49.41:1050',
           'VgR6Xh:tniX7wgDEk@188.130.210.172:1050',
           'VgR6Xh:tniX7wgDEk@109.248.128.89:1050',
           'VgR6Xh:tniX7wgDEk@188.130.210.248:1050',
           'VgR6Xh:tniX7wgDEk@46.8.14.14:1050',
           'VgR6Xh:tniX7wgDEk@45.140.55.25:1050',
           'VgR6Xh:tniX7wgDEk@46.8.111.84:1050',
           'VgR6Xh:tniX7wgDEk@212.115.49.167:1050',
           'VgR6Xh:tniX7wgDEk@45.11.21.172:1050',
           'qQAkG8Sn:DL3PCzyh@5.183.129.141:56485',
           'qQAkG8Sn:DL3PCzyh@45.87.255.149:50015',
           'qQAkG8Sn:DL3PCzyh@45.87.255.189:50015',
           'qQAkG8Sn:DL3PCzyh@45.89.70.158:56779',
           'qQAkG8Sn:DL3PCzyh@92.119.162.117:46965',
           'qQAkG8Sn:DL3PCzyh@45.134.25.124:49457',
           'qQAkG8Sn:DL3PCzyh@91.188.228.181:45539',
           'qQAkG8Sn:DL3PCzyh@91.188.228.239:45539',
           'qQAkG8Sn:DL3PCzyh@91.188.230.151:61009',
           'qQAkG8Sn:DL3PCzyh@194.156.107.237:47668',
           'qQAkG8Sn:DL3PCzyh@45.145.170.52:58393',
           'qQAkG8Sn:DL3PCzyh@193.31.5.101:46320',
           'qQAkG8Sn:DL3PCzyh@193.31.5.102:46320',
           'qQAkG8Sn:DL3PCzyh@193.31.5.148:46320',
           'qQAkG8Sn:DL3PCzyh@77.83.2.153:56009',
           'qQAkG8Sn:DL3PCzyh@45.139.127.67:63837',
           'qQAkG8Sn:DL3PCzyh@45.146.230.99:57548',
           'qQAkG8Sn:DL3PCzyh@176.222.56.181:45167',
           'qQAkG8Sn:DL3PCzyh@176.222.56.247:45167',
           'qQAkG8Sn:DL3PCzyh@45.147.13.14:57132',
           'qQAkG8Sn:DL3PCzyh@176.222.57.5:53950',
           'qQAkG8Sn:DL3PCzyh@176.222.57.54:53950',
           'qQAkG8Sn:DL3PCzyh@45.147.14.115:55014',
           'qQAkG8Sn:DL3PCzyh@45.138.214.4:49468',
           'qQAkG8Sn:DL3PCzyh@45.138.214.87:49468',
           'qQAkG8Sn:DL3PCzyh@45.142.73.53:64624',
           'qQAkG8Sn:DL3PCzyh@45.142.73.95:64624',
           'qQAkG8Sn:DL3PCzyh@194.32.222.35:52531',
           'qQAkG8Sn:DL3PCzyh@194.50.73.56:46814',
           'qQAkG8Sn:DL3PCzyh@45.135.177.249:58692']
usernames = [
    'charlidamelio',
    'addisonre',
    'lorengray',
    'babyariel',
    'zachking',
    'kristenhancher',
    'jacobsartorius',
    'gilmhercroes',
    'flighthouse',
    'jaydencroes'
]
# Since TikTok changed their API you need to use the custom_verifyFp option.
# In your web browser you will need to go to TikTok, Log in and get the s_v_web_id value.
# while True:
results_count = 30

for username, proxy in zip(usernames, proxies[len(usernames):2 * len(usernames)]):
    tiktocks = api.getUser(username=username,
                              count=results_count,
                              custom_verifyFp='',
                              language='en',
                              proxy='http://' + proxy)

    time.sleep(random.random())
    with open(f'data/2_{username}.json', 'w') as f:
        f.write(json.dumps(tiktocks, indent=4))
    print(f'Loaded {len(tiktocks["items"])} tiktoks by @{username}')
