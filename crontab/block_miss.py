import logging
import sys
import datetime
from backend.block_product.block_miss import BlockMiss
from autoapp import app

taskname = "block miss"
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            time_str = sys.argv[1]
            utc_date_time = datetime.datetime.strptime(time_str, "%Y-%m-%d")
        else:
            utc_date_time = datetime.datetime.now() - datetime.timedelta(days=1)
        with app.app_context():
            miss = BlockMiss(utc_date_time)
            miss.calc()
            miss.format()
            logging.info('execute crontab [%s] success. Date: %s', taskname, miss.utc_date_time)
    except Exception as e:
        logging.error('execute crontab [%s] error: %s', taskname, e)