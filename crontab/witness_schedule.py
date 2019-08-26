import sys
import logging
import datetime
from backend.block import operations
from scripts import witness_service

taskname = "witness schedule"
if __name__ == "__main__":

    try:
        if len(sys.argv) > 1:
            time_str = sys.argv[1]
            utc_date_time = datetime.datetime.strptime(time_str, "%Y-%m-%d")
        else:
            utc_date_time = datetime.datetime.now() - datetime.timedelta(days=1)
        witness_service.witness_services("make_witness_schedule", utc_date_time)
        logging.info('execute crontab [%s] success.', taskname)
    except Exception as e:
        logging.error('execute crontab [%s] error: %s', taskname, e)