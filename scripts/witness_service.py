# This module contains scripts as follows:
# 1.make_witness_schedule: create four witness_schedule records every day. it will update the db table witness schedule.
# 2.witness_miss_block_by_day: analyze the miss block in given day.
# 
# [how to use]
# python -m scripts.witness_service func params
# func: it is must one of const_func_available.
# params: the params needed by func.
import sys
import logging
from datetime import datetime as dt
from autoapp import app
from backend.witness.operations import make_witness_schedule, witness_miss_block_by_day, witness_miss_block_by_period

# define the supported command
const_func_available = {'make_witness_schedule', 'witness_miss_block_by_day', 'witness_miss_block_by_period', 'make_witness_schedule_period'}

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

if __name__ == '__main__':
    try:
        func, params = parse_args()
        utc_date_time = dt.utcfromtimestamp(int(params[0]))
    except Exception as e:
        logging.error('parse_args error: %s', e)
    try:
        with app.app_context():
            if func == 'make_witness_schedule':
                make_witness_schedule(utc_date_time, index=None)
            elif func == 'make_witness_schedule_period':
                make_witness_schedule_period(utc_date_time, index="1")
            elif func == 'witness_miss_block_by_day':
                logging.info(witness_miss_block_by_day(utc_date_time, index=None))
            elif func == 'witness_miss_block_by_period':
                logging.info(witness_miss_block_by_day(utc_date_time, index="1"))
    except Exception as e:
        logging.error('execute script error: %s', e)
        