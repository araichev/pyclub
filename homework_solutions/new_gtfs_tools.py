"""
This module defines a ``Feed`` class to represent GTFS feeds.
There is an instance attribute for every valid GTFS table (routes, stops, etc.), which stores the table as a Pandas DataFrame, or as ``None`` in case that table is missing.

The ``Feed`` class also has heaps of methods: a method to compute route stats, a method to compute screen line counts, validations methods, etc.
To ease reading, almost all of these methods are defined in other modules and grouped by theme (``routes.py``, ``stops.py``, etc.).
These methods, or rather functions that operate on feeds, are then imported within the ``Feed`` class.
However, this separation of methods messes up the ``Feed`` class documentation slightly by introducing an extra leading ``feed`` parameter in the method signatures.
Ignore that extra parameter; it refers to the ``Feed`` instance, usually called ``self`` and usually hidden automatically by documentation tools.

Conventions in the code below:
    - Dates are encoded as date strings of the form YYMMDD
    - Times are encoded as time strings of the form HH:MM:SS with the possibility that the hour is greater than 24
    - 'DataFrame' and 'Series' refer to Pandas DataFrame and Series objects, respectively
"""
from pathlib import Path
import tempfile
import shutil
from collections import OrderedDict

import pandas as pd
import shapely.geometry as sg


class Feed(object):
    """
    An instance of this class represents a not-necessarily-valid GTFS feed, where GTFS tables are stored as DataFrames.
    Beware that the stop times DataFrame can be big (several gigabytes), so make sure you have enough memory to handle it.

    Public instance attributes:

    - ``agency``
    - ``stops``
    - ``routes``
    - ``trips``
    - ``stop_times``
    - ``calendar``
    - ``calendar_dates``
    - ``fare_attributes``
    - ``fare_rules``
    - ``shapes``
    - ``frequencies``
    - ``transfers``
    - ``feed_info``
    """
    gtfs_tables = [
        'agency',
        'calendar',
        'calendar_dates',
        'fare_attributes',
        'fare_rules',
        'feed_info',
        'frequencies',
        'routes',
        'shapes',
        'stops',
        'stop_times',
        'trips',
        'transfers',
        ]

    str_fields= [
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
      'parent_station',
    ]

    def __init__(self, agency=None, stops=None, routes=None,
      trips=None, stop_times=None, calendar=None, calendar_dates=None,
      fare_attributes=None, fare_rules=None, shapes=None,
      frequencies=None, transfers=None, feed_info=None):
        """
        Assume that every non-None input is a Pandas DataFrame.
        No formats are checked.
        In particular, a Feed instance need not represent a valid GTFS feed.
        """
        # Set primary attributes; the @property magic below will then
        # validate some and automatically set secondary attributes
        for prop, val in locals().items():
            if prop in Feed.gtfs_tables:
                setattr(self, prop, val)
                
    def __str__(self):
        d = OrderedDict()
        for table in Feed.gtfs_tables:
            try:
                d[table] = getattr(self, table).head(5)
            except:
                d[table] = None
        return '\n'.join(['* {!s} --------------------\n\t{!s}'.format(k, v) for k, v in d.items()])

    def build_geometry_by_shape(self, shape_ids=None):
        """
        Given a GTFS feed object, return a dictionary with structure 
        shape ID -> Shapely LineString representation of shape,
        where the dictionary ranges over all shapes in the feed.
        Use WGS84 longitude-latitude coordinates, the native coordinate system of GTFS.

        If a list of shape IDs ``shape_ids`` is given, 
        then only include the given shape IDs in the dictionary.

        NOTES:
            - Raise a ValueError if the feed has no shapes
        """
        if self.shapes is None:
            raise ValueError('This feed has no shapes')

        d = dict()
        sh = self.shapes.copy()

        # Restrict shapes if necessary
        if shape_ids is not None:
            sh = sh[sh['shape_id'].isin(shape_ids)]

        sh = sh.sort_values(['shape_id', 'shape_pt_sequence'])

        for shid, group in sh.groupby('shape_id'):
            lonlats = group[['shape_pt_lon', 'shape_pt_lat']].values
            d[shid] = sg.LineString(lonlats)

        return d

    def trip_to_geojson(self, trip_id):
        """
        Given a GTFS feed object and a trip ID from that feed,
        return a GeoJSON LineString feature (as a Python dictionary)
        representing the trip's geometry and its metadata
        (trip ID, direction ID, headsign, etc.).
        Use WGS84 coordinates, the native coordinate system of GTFS.

        NOTES:
            Raise a ``ValueError`` if the appropriate GTFS data does not exist.
        """
        if trip_id not in self.trips['trip_id'].values:
            raise ValueError('Trip ID {!s} not present in feed trips'.format(trip_id))

        # Get trip data as dictionary, replacing numpy.nan with 'n/a' to ease later
        # conversion to JSON
        t = self.trips.copy()
        d = t[t['trip_id'] == trip_id].fillna('n/a').to_dict(orient='records')[0]

        # Get Shapely LineString for trip shape
        shid = d['shape_id']
        geom = self.build_geometry_by_shape(shape_ids=[shid])[shid]

        # Convert LineString to GeoJSON format
        result = {
            'type': 'Feature', 
            'properties': d,
            'geometry': sg.mapping(geom),
        }
        return result

    def compute_screen_line_counts(self, linestring):
        """
        Find all trips in the given GTFS self object that intersect the given Shapely LineString
        (given in WGS84 coordinates), and return a data frame with the columns:

        - ``'trip_id'``
        - ``'route_id'``
        - ``'route_short_name'``
        - ``'direction_id'``
        - ``'shape_id'``
        """
        # Convert all shapes to linestrings
        geometry_by_shape = self.build_geometry_by_shape()

        # Interate through linestrings to find intersections with screenline
        hits = []
        for shid, geom in geometry_by_shape.items():
            if geom.intersects(linestring):
                hits.append(shid)

        # Compile trip info for hits
        t = self.trips.copy()
        t = t[t['shape_id'].isin(hits)].copy()
        result = t.merge(self.routes) # Add more route info

        return result[['trip_id', 'route_id', 'route_short_name', 'direction_id', 'shape_id']]

def read_gtfs(path):
    """
    Given a path (string or pathlib object) to a (zipped) GTFS feed,
    read the feed and return its corresponding Feed instance.

    NOTES:
        - Ignore files that are not valid GTFS; see https://developers.google.com/transit/gtfs/reference/.
        - Ensure that all ID fields that could be string ('stop_id', 'route_id', etc.) are parsed as strings and not as numbers.    
    """
    path = Path(path)
    
    # Unzip feed into temporary directory
    tmp_dir = tempfile.TemporaryDirectory()
    shutil.unpack_archive(str(path), tmp_dir.name, 'zip')

    # Read valid GTFS files into Pandas data frames
    feed_dict = {}
    dtype = {field: str for field in Feed.str_fields} # ensure some string types
    for p in Path(tmp_dir.name).iterdir():        
        name = p.stem
        if name in Feed.gtfs_tables:
            feed_dict[name] = pd.read_csv(p, dtype=dtype)
        
    # Delete temporary directory
    tmp_dir.cleanup()
    
    return Feed(**feed_dict)