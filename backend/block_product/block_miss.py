import logging
from pprint import pprint

from datetime import datetime as dt
from backend.witness import operations as witness_op
from backend.block import operations as block_op

def print_witness_miss_block(date, missblock_oneday, maintaince_slot_timestamp):
    witness_list = witness_op.query_witness(missblock_oneday.keys())

    total_miss = 0
    for witness, blocks in missblock_oneday.items():
        blocks = list(set(blocks) - maintaince_slot_timestamp)  # exclude the maintaince timestamp
        if witness_list.get(witness):
            if blocks:
                logging.debug("%s missed %d block: %s", witness_list.get(witness), len(blocks), ','.join([str(item) for item in blocks]))
                total_miss = total_miss + len(blocks)
        else:
            logging.warn("witness %s is missing.", witness)
            if blocks:
                logging.debug("%s missed %d block: %s", witness, len(blocks), ','.join([str(item) for item in blocks]))
                total_miss = total_miss + len(blocks)

    logging.debug("total_miss: %d", total_miss)
    return  total_miss, missblock_oneday

def calc_maintaince_slot_timestamp(utc_date_time):
    maintaince_slot_timestamp = set()
    four_period = witness_op.four_period_one_day(utc_date_time)
    for item in four_period:
        maintaince_slot_timestamp.add(item[1] - 3)
        maintaince_slot_timestamp.add(item[1] - 6)

    temp = list(maintaince_slot_timestamp)
    temp.sort()
    logging.info("maintaince slot_timestamps are %s", ",".join(map(lambda x: str(x), temp)))
    return maintaince_slot_timestamp

def calc_missblock_timestamp_height(timestamp_list=None):
    timestamp_number = {}
    if not timestamp_list:
        return dict()
    
    timestamp_list.sort()
    for timestamp in timestamp_list:
        block = block_op.query_block_near_timestamp(timestamp, "after")
        timestamp_number[timestamp] = block.number

    return timestamp_number

class BlockMiss(object):

    period_witness_scedule = {}
    missblock_oneday = {}
    utc_date_time = None
    total_miss = 0
    maintaince_slot_timestamp = set()  # 维护期不出块的slot对应的timestamp, 每个维护期有2个不出块的slot
    
    miss_block_timestamp = []
    missblock_timestamp_height = {}

    witness_list = None

    def __init__(self, utc_date_time):
        self.utc_date_time = utc_date_time
        self.maintaince_slot_timestamp = calc_maintaince_slot_timestamp(utc_date_time)

    def calc(self):
        if self._check():
            witness_miss_block_by_day = witness_op.witness_miss_block_by_day(self.utc_date_time)
            for period, miss_block_dict in witness_miss_block_by_day.items():
                for witness, miss_blocks in miss_block_dict.items():
                    if not self.missblock_oneday.get(witness):
                        self.missblock_oneday[witness] = miss_blocks
                    else:
                        self.missblock_oneday[witness].extend(miss_blocks)

            self.witness_list = witness_op.query_witness(self.missblock_oneday.keys())

            # exclude the maintaince timestamp
            for witness, blocks in self.missblock_oneday.items():
                actual_blocks = list(set(blocks) - self.maintaince_slot_timestamp)
                if self.witness_list.get(witness):
                    if actual_blocks:
                        self.total_miss += len(actual_blocks)
                else:
                    logging.warn("witness %s is missing.", witness)
                    if actual_blocks:
                        self.total_miss += len(actual_blocks)
                self.missblock_oneday[witness] = actual_blocks

            self.miss_block_timestamp = list(sum(list(self.missblock_oneday.values()), []))
            self.missblock_timestamp_height = calc_missblock_timestamp_height(self.miss_block_timestamp)
            return True
        return False
        
    def _check(self):
        # check witness schedule available
        four_period = witness_op.four_period_one_day(self.utc_date_time)
        for item in four_period:
            schedule = witness_op.witness_schedule_by_period(item[0], item[1])
            if not schedule:
                return False
        return True

    def format(self):
        details = ""
        for witness, blocks in self.missblock_oneday.items():
            if len(blocks) > 0:
                witness_name = witness if not self.witness_list.get(witness) else self.witness_list.get(witness).name
                details += "%2d: %-24.20s %s\n" % (len(blocks), witness_name, ",".join([str(self.missblock_timestamp_height.get(block)) for block in blocks]))

        output = "Date: %s UTC+0:00 \nTotal Miss Block: %d \nDetails:\n%s" % (str(self.utc_date_time.date()), self.total_miss, details)
        print(output)


