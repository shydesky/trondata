import sys
import logging
import time
import functools
from datetime import datetime, timezone, timedelta
from backend.exceptions.error import InputError, LogicError
from backend.witness.models import Witness, WitnessSchedule
from backend.database import db

from backend.block.operations import query_block_by_timestamp, query_block_near_timestamp, query_block_by_number

def get_all_witness():
    witness_list = db.session.query(Witness).all()
    return witness_list

def _make_witness_schedule(utc_date_time, index=1):
    t0 = time.time()
    year, month, day = utc_date_time.timetuple()[:3]
    if index == 1:
        t_start = int(datetime(year, month, day, 0, 0, 12, tzinfo=timezone.utc).timestamp())
        t_end = int(datetime(year, month, day, 6, 0, 9, tzinfo=timezone.utc).timestamp())
    elif index == 2:
        t_start = int(datetime(year, month, day, 6, 0, 12, tzinfo=timezone.utc).timestamp())
        t_end = int(datetime(year, month, day, 12, 0, 9, tzinfo=timezone.utc).timestamp())
    elif index == 3:
        t_start = int(datetime(year, month, day, 12, 0, 12, tzinfo=timezone.utc).timestamp())
        t_end = int(datetime(year, month, day, 18, 0, 9, tzinfo=timezone.utc).timestamp())
    elif index == 4:
        t_start = int(datetime(year, month, day, 18, 0, 12, tzinfo=timezone.utc).timestamp())
        year, month, day = (utc_date_time + timedelta(days=1)).timetuple()[:3]
        t_end = int(datetime(year, month, day, 0, 0, 9, tzinfo=timezone.utc).timestamp())
    
    b_start = query_block_near_timestamp(timestamp=t_start, near_type="after")
    b_end = query_block_near_timestamp(timestamp=t_end, near_type="before")

    if not b_start and not b_end:
        raise LogicError("not near timestamp block", "")
    witness_list = calc_witness_list(t_start, b_start.number)
    
    logging.info('time: %s ms', (time.time() - t0)*1000)
    return dict(timestamp_start=t_start, timestamp_end=t_end, witness_list=witness_list, block_number_start=b_start.number, block_number_end=b_end.number)

# define the 4 functions to handle four period in one day.
make_witness_schedule1 = functools.partial(_make_witness_schedule, index=1)
make_witness_schedule2 = functools.partial(_make_witness_schedule, index=2)
make_witness_schedule3 = functools.partial(_make_witness_schedule, index=3)
make_witness_schedule4 = functools.partial(_make_witness_schedule, index=4)


# 按天根据每个维护期的产块情况计算witness的出块顺序，写入WitnessSchedule，每天4条数据
def make_witness_schedule(utc_date_time, index=None):
    if not isinstance (utc_date_time, datetime):
        utc_date_time = datetime.utcnow()
    index = "1234" if not index else index

    logging.info('make witness schedule(%s) start.', utc_date_time.date())

    try:
        if "1" in index:
            wit_dict = make_witness_schedule1(utc_date_time)
            WitnessSchedule.create_from_dict(wit_dict, need_to_commit=False)
            logging.info(wit_dict)

        if "2" in index:
            wit_dict = make_witness_schedule2(utc_date_time)
            WitnessSchedule.create_from_dict(wit_dict, need_to_commit=False)
            logging.info(wit_dict)

        if "3" in index:
            wit_dict = make_witness_schedule3(utc_date_time)
            WitnessSchedule.create_from_dict(wit_dict, need_to_commit=False)
            logging.info(wit_dict)

        if "4" in index:
            wit_dict = make_witness_schedule4(utc_date_time)
            WitnessSchedule.create_from_dict(wit_dict, need_to_commit=False)
            logging.info(wit_dict)
        db.session.commit()
        logging.info('make witness schedule(%s) success.', utc_date_time.date())

    except Exception as e:
        db.session.rollback()
        logging.error('make witness schedule(%s) failure.', utc_date_time.date())


def calc_witness_list(t_start, number):
    witness_list = [None] * 27
    base_timestamp = t_start 
    blocks = query_block_by_number(number, number + 500)
    if not blocks:
        logging.error('no blocks fetched after time %d, please fetch block at first.', base_timestamp)
        raise LogicError(base_timestamp, 'blocks size:{}'.format(len(blocks)))# to do
    while True:
        for block in blocks:
            index = int((block.timestamp - base_timestamp) / 3 % 27)
            witness_list[index] = block.witness_address
            if None not in witness_list:
                sorted_witness = ",".join(witness_list)
                logging.info(str(base_timestamp) + ":" + sorted_witness)
                return sorted_witness
        logging.error('%s ~ %s do not contain 27 witnesses!', blocks[0].number, blocks[-1].number)
        raise LogicError('not contain 27 witnesses', 'knowned witness_list: {}'.format(",".join(witness_list)))

def four_period_one_day(utc_date_time):
    res = []
    year, month, day = utc_date_time.timetuple()[:3]

    t_start = int(datetime(year, month, day, 0, 0, 12, tzinfo=timezone.utc).timestamp())
    t_end = int(datetime(year, month, day, 6, 0, 9, tzinfo=timezone.utc).timestamp())
    res.append((t_start, t_end))
    
    t_start = int(datetime(year, month, day, 6, 0, 12, tzinfo=timezone.utc).timestamp())
    t_end = int(datetime(year, month, day, 12, 0, 9, tzinfo=timezone.utc).timestamp())
    res.append((t_start, t_end))
    
    t_start = int(datetime(year, month, day, 12, 0, 12, tzinfo=timezone.utc).timestamp())
    t_end = int(datetime(year, month, day, 18, 0, 9, tzinfo=timezone.utc).timestamp())
    res.append((t_start, t_end))
    
    t_start = int(datetime(year, month, day, 18, 0, 12, tzinfo=timezone.utc).timestamp())
    year, month, day = (utc_date_time + timedelta(days=1)).timetuple()[:3]
    t_end = int(datetime(year, month, day, 0, 0, 9, tzinfo=timezone.utc).timestamp())
    res.append((t_start, t_end))

    return res

#按天统计witness丢块情况
def witness_miss_block_by_day(utc_date_time, index=None):
    index = "1234" if not index else index
    witness_miss_block_by_day = dict()
    year, month, day = utc_date_time.timetuple()[:3]

    if "1" in index:
        t_start = int(datetime(year, month, day, 0, 0, 12, tzinfo=timezone.utc).timestamp())
        t_end = int(datetime(year, month, day, 6, 0, 9, tzinfo=timezone.utc).timestamp())
        witness_miss_dict = witness_miss_block_by_period(t_start, t_end)
        witness_miss_block_by_day[(t_start, t_end)] = witness_miss_dict

    if "2" in index:
        t_start = int(datetime(year, month, day, 6, 0, 12, tzinfo=timezone.utc).timestamp())
        t_end = int(datetime(year, month, day, 12, 0, 9, tzinfo=timezone.utc).timestamp())
        witness_miss_dict = witness_miss_block_by_period(t_start, t_end)
        witness_miss_block_by_day[(t_start, t_end)] = witness_miss_dict

    if "3" in index:
        t_start = int(datetime(year, month, day, 12, 0, 12, tzinfo=timezone.utc).timestamp())
        t_end = int(datetime(year, month, day, 18, 0, 9, tzinfo=timezone.utc).timestamp())
        witness_miss_dict = witness_miss_block_by_period(t_start, t_end)
        witness_miss_block_by_day[(t_start, t_end)] = witness_miss_dict

    if "4" in index:
        t_start = int(datetime(year, month, day, 18, 0, 12, tzinfo=timezone.utc).timestamp())
        year, month, day = (utc_date_time + timedelta(days=1)).timetuple()[:3]
        t_end = int(datetime(year, month, day, 0, 0, 9, tzinfo=timezone.utc).timestamp())
        witness_miss_dict = witness_miss_block_by_period(t_start, t_end)
        witness_miss_block_by_day[(t_start, t_end)] = witness_miss_dict

    return witness_miss_block_by_day


#按维护期统计witness丢块情况
def witness_miss_block_by_period(t_start, t_end):
    schedule = WitnessSchedule.query.filter(WitnessSchedule.timestamp_start==t_start, WitnessSchedule.timestamp_end==t_end).first()
    blocks = query_block_by_timestamp(timestamp_start=t_start, timestamp_end=t_end)
    if not schedule:
        raise LogicError('no witness schedule in {} ~ {}'.format(t_start, t_end), "")
    witness_list = schedule.witness_list.split(',')
    witness_miss_dict = {witness: [] for witness in witness_list}

    logging.info("%s ~ %s produce %d block expected, but actually produce %d blocks, missed %d blocks", t_start, t_end, (t_end - t_start) /3 + 1, len(blocks), (t_end - t_start) /3 + 1 - len(blocks))
    index = 0
    for time in range(int(t_start), int(t_end), 3):
        block = blocks[index]
        if time == block.timestamp:
            index = index + 1
            continue
        else:
            ss = int((time - t_start) / 3 % 27)
            witness_miss_dict[witness_list[ss]].append(time)
    ll = []
    for key, value in witness_miss_dict.items():
        ll.extend(value)
    ll.sort()
    logging.info('the timestamp of the missed blocks are %s, total number is %d', ','.join(map(lambda x: str(x),ll)), len(ll))
    return witness_miss_dict

def witness_schedule_by_period(t_start, t_end):
    schedule = WitnessSchedule.query.filter(WitnessSchedule.timestamp_start==t_start, WitnessSchedule.timestamp_end==t_end).first()
    return schedule

def query_witness(witness_address_list=None, res_key=None):
    query = db.session.query(Witness)
    if witness_address_list:
        query.filter(Witness.address.in_(witness_address_list))
    witnesses = query.all()
    if res_key == 'address_b58c':
        return {item.address_b58c: item for item in witnesses}
    else:
        return {item.address: item for item in witnesses}

