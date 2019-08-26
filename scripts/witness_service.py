import logging
from autoapp import app
from backend.witness import operations

def witness_services(func, utc_date_time):
    with app.app_context():
        if func == 'make_witness_schedule':
            operations.make_witness_schedule(utc_date_time, index=None)
        elif func == 'make_witness_schedule_period':
            operations.make_witness_schedule_period(utc_date_time, index="1")
        elif func == 'witness_miss_block_by_day':
            logging.info(operations.witness_miss_block_by_day(utc_date_time, index=None))
        elif func == 'witness_miss_block_by_period':
            logging.info(operations.witness_miss_block_by_day(utc_date_time, index="1"))
        