import logging
import datetime
from backend.block import operations
from scripts import witness_service

from autoapp import app

taskname = "witness schedule"
if __name__ == "__main__":

    try:
        current_time = datetime.datetime.now() - datetime.timedelta(days=1)
        witness_service.witness_services("make_witness_schedule", current_time)
        logging.info('execute crontab [%s] success.', taskname)
    except Exception as e:
        logging.error('execute crontab [%s] error: %s', taskname, e)