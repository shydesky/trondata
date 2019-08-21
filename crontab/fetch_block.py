import logging
import datetime
from backend.block import operations
from scripts import block_service
from autoapp import app

taskname = "fetch block"
if __name__ == "__main__":

    try:
        current_time = datetime.datetime.now().timestamp()
        with app.app_context():
            head_block = operations.query_block_max()
            if head_block:
                delta = int(current_time) - 81 - head_block.timestamp
                delta_block_num = int(delta / 3)
                beginNumber = head_block.number + 1 # 当前头块的下一块
                endNumber = beginNumber + delta_block_num
                block_service.fetch_block(beginNumber, endNumber)
                logging.info('execute crontab [%s] success. head_block number: %d, beginNumber: %d, endNumber: %d', taskname, head_block.number, beginNumber, endNumber)
    except Exception as e:
        logging.error('execute crontab [%s] error: %s', taskname, e)