import sys
import requests
import logging
import concurrent.futures
from functools import cmp_to_key, wraps
from backend.block import operations
import time

# define the supported command
const_func_available = {'fetch_block', 'other'}

def func_execute_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        logging.debug("%s execute use time: %d seconds.", func.__name__, time.time() - t0)
        return res
    return wrapper

def func_retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = None
        retry = 3
        while retry > 0:
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                logging.error(e)
                retry = retry - 1
            else:
                break
        return res
    return wrapper

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


block_header_start_end = "/wallet/getblockheaderbylimitnext?startNum=%s&endNum=%s"
host_pool = [
    "http://47.89.182.29:8090"
]

def fetch_block_for_trx(beginNumber, endNumber):
    to_do = []
    results = []
    step = int((endNumber - beginNumber)) / 50
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

# usage:  request block from FullNode by HTTP api and save them in database. 
# params: @beginNumber the begin height of block 
#         @endNumber the end height of block
@func_execute_time
def fetch_block(beginNumber, endNumber):
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        step = 50
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
    t1 = time.time()
    logging.debug("fetch block use time: %d", t1 - t0)

    #results.sort(key=cmp_to_key(lambda a, b: a.number - b.number))
    t2 = time.time()
    operations.sync_block(blocks=results)
    t3 = time.time()
    logging.debug("insert db use time: %d", t3 - t2)
    return True

@func_retry
def getBlockLimitNext(args):
    block_list = []
    url = (host_pool[args[2]] + block_header_start_end) % (args[0], args[1])
    logging.debug(url)    
    res = requests.get(url, timeout=100)
    if res.ok:
        for item in res.json().get("block"):
            block_list.append(item)
    else:
        raise
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
            elif func == 'other':
                pass
    except Exception as e:
        logging.error('execute script error: %s', e)




        