import requests
import concurrent.futures
from functools import cmp_to_key

from backend.account import operations

block_start_end = "/wallet/getblockheaderbylimitnext?startNum=%s&endNum=%s"
# host_pool = [
#     "http://api.trongrid.io", 
#     "http://54.236.37.243:8090", 
#     "http://52.53.189.99:8090", 
#     "http://18.196.99.16:8090", 
#     "http://34.253.187.192:8090",
#     "http://52.56.56.149:8090",
#     "http://35.180.51.163:8090",
#     "http://54.252.224.209:8090",
#     "http://18.228.15.36:8090",
#     "http://52.15.93.92:8090",
#     "http://34.220.77.106:8090",
#     "http://13.127.47.162:8090",
#     "http://13.124.62.58:8090"
# ]

host_pool = [
    "http://localhost:8090"
]

def fetch_block(beginNumber, endNumber):
    to_do = []
    results = []
    step = 100
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        i = 0
        for item in range(beginNumber, endNumber, step):
            i = i % len(host_pool)
            to_do.append(executor.submit(getBlockLimitNext, (item, min(endNumber, item + step), i)))
            i = i + 1

    for future in concurrent.futures.as_completed(to_do):
        res = future.result()
        results.extend(res)

    #results.sort(key=cmp_to_key(lambda a, b: a.number - b.number))
    operations.sync_block(blocks=results)
    return True

def getBlockLimitNext(args):
    block_list = []
    retry = 3
    url = (host_pool[args[2]] + block_start_end) % (args[0], args[1])
    print(url)
    while retry > 0:
        try:
            res = requests.get(url, timeout=100)
            if res.ok:
                for item in res.json().get("block"):
                    block_list.append(item)
            else:
                raise
        except Exception as e:
            retry = retry - 1
        else:
            break
    
    return block_list

if __name__ == "__main__":
    beginNumber = 0
    endNumber = 100
    from backend.app import create_app
    from backend.settings import DevConfig

    app = create_app(DevConfig)
    with app.app_context():
        fetch_block(beginNumber, endNumber)


        from backend.app import create_app
        from backend.settings import DevConfig
        import time
        app = create_app(DevConfig)
        with app.app_context():
            for i in range(52000,100000, 10000):
                print(i, i+10000)
                time.sleep(5)
                fetch_block(i, i+10000)


