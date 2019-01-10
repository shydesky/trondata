import sys
import requests
import logging
import concurrent.futures
from functools import cmp_to_key
from backend.block import operations

def parse_args():
    try:
        func = sys.argv[1]
        params = sys.argv[2:]
    except Exception as e:
        logging.error('unexcepted error: %s', e)
        return
    if not func in const_func_available:
        logging.error('unsupported command: %s', func)
        return
    logging.info("func: %s\nparmas: %s", func, list(map(lambda x: str(x), params)))
    return func, params

# define the supported command
const_func_available = {'fetch_block'}

block_header_start_end = "/wallet/getblockheaderbylimitnext?startNum=%s&endNum=%s"
host_pool = [
    "http://47.90.210.159:8090"
]

def fetch_block_for_trx(beginNumber, endNumber):
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
        logging.debug("block len: %d", len(results))
    return results

def fetch_block(beginNumber, endNumber):
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        step = 100
        to_do = []
        i = 0
        for item in range(beginNumber, endNumber, step):
            i = i % len(host_pool)
            to_do.append(executor.submit(getBlockLimitNext, (item, min(endNumber, item + step), i)))
            i = i + 1

    results = []
    for future in concurrent.futures.as_completed(to_do):
        res = future.result()
        results.extend(res)
        logging.debug("block len: %d", len(results))

    #results.sort(key=cmp_to_key(lambda a, b: a.number - b.number))
    operations.sync_block(blocks=results)
    return True

def getBlockLimitNext(args):
    block_list = []
    retry = 3
    url = (host_pool[args[2]] + block_header_start_end) % (args[0], args[1])
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
    from autoapp import app
    try:
        func, params = parse_args()
        beginNumber = int(params[0])
        endNumber = int(params[1])
    except Exception as e:
        logging.error('parse_args error: %s', e)

    try:
        with app.app_context():
            if func == 'fetch_block':
                fetch_block(beginNumber, endNumber)
    except Exception as e:
        logging.error('execute script error: %s', e)




        