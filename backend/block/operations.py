import logging
from sqlalchemy import desc
from backend.block.models import Block
from backend.database import db
from backend.dto.blockdto import BlockDTO

def get_block_list(start, end):
    block_list = db.session.query(Block).filter(Block.number.in_(range(start, end))).all()
    return block_list

# batch insert block
def batch_sync_block(blocks=None):
    if not blocks:
        return
    if not isinstance(blocks, list):
        blocks = [blocks]
    objects = []
    for block in blocks:
        try:
            objects.append(BlockDTO.convert(block))
        except Exception as e:
            continue
    step = 5000
    for item in range(0, len(objects), step):
        try:
            db.session.bulk_insert_mappings(Block, objects[item: min(item + step, len(objects))])        
            db.session.commit()
        except Exception as e:
            db.session.rollback()


def sync_block(blocks=None):
    if not blocks:
        return
    if not isinstance(blocks, list):
        blocks = [blocks]
    for block in blocks:
        try:
            Block.create_from_dict(BlockDTO.convert(block), need_to_commit=False)
        except Exception as e:
            db.session.rollback()
        else:
            db.session.commit()

# query a block near the given timestamp with the specified near_type 
def query_block_near_timestamp(timestamp, near_type=None):
    if not near_type or not near_type in ("before", "after"):
        near_type = "after"

    block = None
    count = 0
    while count < 27:
        if near_type == 'after':
            print(timestamp)
            print(timestamp - count*3)
            block = Block.query.filter_by(timestamp=timestamp + count*3).first()
            if block:
                break
        elif near_type == 'before':
            block = Block.query.filter_by(timestamp=timestamp - count*3).first()
            if block:
                break
        count = count + 1
    return block

def query_block_by_number(number_start, number_end):
    query = db.session.query(Block).filter(Block.number.in_(range(number_start, number_end)))
    blocks = query.order_by(Block.number).all()
    logging.debug(query.statement)
    return blocks


def query_block_by_timestamp(timestamp_start=None, timestamp_end=None, limit=None):
    query = db.session.query(Block)
    if timestamp_start:
        query = query.filter(Block.timestamp >= timestamp_start)
    if timestamp_end:
        query = query.filter(Block.timestamp <= timestamp_end)
    query = query.order_by(Block.number)
    if limit:
        query = query.limit(limit)
    blocks = query.all()
    return blocks

def query_block_max():
    query = db.session.query(Block).order_by(desc(Block.number)).limit(1)
    head_block = query.first()
    return head_block
