```shell
cd path/to/root

# fetch blocks
python -m scripts.fetch_block fetch_block beginNumber endNumber
# make_witness_schedule
# utc_date_time is the time from 1970-1-1 00:00:00 UTC+0 seconds
python -m scripts.witness_service make_witness_schedule utc_date_time
# witness_miss_block_by_day
# utc_date_time is the time from 1970-1-1 00:00:00 UTC+0 seconds
python -m scripts.witness_service witness_miss_block_by_day utc_date_time
```

```shell
#this is an example for how to get the utc_date_time.
#import datetime
#utc_date_time = datetime.datetime(2019, 1, 10, 0, 0, 0, tzinfo=datetime.timezone.utc).timestamp()
```