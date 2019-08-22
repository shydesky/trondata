import logging
import datetime
from backend.block_product.block_miss import BlockMiss
from autoapp import app

taskname = "block miss"
if __name__ == "__main__":

    try:
        current_time = datetime.datetime.now() - datetime.timedelta(days=1)
        with app.app_context():
            miss = BlockMiss(current_time)
            miss.calc()
            miss.format()
            logging.info('execute crontab [%s] success. Date: %s', taskname, miss.utc_date_time)
    except Exception as e:
        logging.error('execute crontab [%s] error: %s', taskname, e)