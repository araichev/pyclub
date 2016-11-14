from pathlib import Path
import shutil

import pandas as pd
import numpy as np


GTFS_TABLES = [
    'agency',
    'stops',
    'routes',
    'trips',
    'stop_times',
    'calendar',
    'calendar_dates',
    'fare_attributes',
    'fare_rules',
    'shapes',
    'frequencies',
    'transfers',
    'feed_info',
    ]

STR_FIELDS = [
  'agency_id'
  'trip_id',
  'service_id',
  'shape_id',
  'block_id',
  'route_id',
  'stop_id',
  'fare_id',
  'origin_id',
  'destination_id',
  'contains_id',
  'from_stop_id',
  'to_stop_id',
]

def read_gtfs(path):
    """
    Given a path (string or pathlib object) to a (zipped) GTFS feed,
    unzip the feed and save the files to a dictionary whose keys are
    named after GTFS tables ('stops', 'routes', etc.) and whose
    corresponding values are Pandas data frames representing the tables.
    Return the resulting dictionary.

    NOTES:
        - Ignore files that are not valid GTFS; see https://developers.google.com/transit/gtfs/reference/.
        - Ensure that all ID fields that could be string ('stop_id', 'route_id', etc.) are parsed as strings and not as numbers.    
    """
    path = Path(path)
    
    # Unzip feed
    extract_dir = path.with_name(path.stem)
    shutil.unpack_archive(str(path), str(extract_dir), 'zip')

    # Read files into Pandas data frames
    feed = {}
    dtype = {field: str for field in STR_FIELDS} # ensure some string types
    for p in extract_dir.iterdir():
        name = p.stem
        
        # Skip invalid files
        if name not in GTFS_TABLES:
            continue
        
        # Read valid files
        feed[name] = pd.read_csv(p, dtype=dtype)
        
    # Delete temporary directory
    shutil.rmtree(str(extract_dir))
    
    return feed