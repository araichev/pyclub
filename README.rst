PyClub 
*******
This is a repository of supporting material for PyClub, a work-time meetup about Python and data science at MRCagney.


Introduction
=============
- Motivation: Upskill on Python for data science. Python is useful, data science is useful, and the two together are a powerful combination.

- Focus: Tools and processes for analyzing transit and geospatial data, because that's our main work at MRCagney

- Assumption: You have Python proficiency at the level of, say, the `Codeacademy Python 2 tutorial <https://www.codecademy.com/learn/python>`_. We will be using Python 3, but they're not too different.

- Third-party Python libraries that we will use a lot:

  * NumPy for numerical computing
  * Pandas for tabular data
  * Shapely and Fiona for geospatial data
  * Geopandas, which combines Shapely with Pandas
  * GTFSTK for GTFS feeds

- Other notable third-party Python libraries for data science:
  
  * SciPy for scientific/engineering computing
  * Matplotlib and Seaborn for plotting and (static) visualization.
  * Statsmodels for statistical modeling
  * Scikit-Learn for machine learning
  * Requests for API calls
  * Scrapy for web crawling and scraping


Homework 1
===========
| Theme: Set up and warm up
| Due: 2016-11-01

1. On your computer, install Python 3.5, a virtual environment manager, and a Python package manager. You can do all this at once in a straightforward and cross-platform way by installing `Anaconda <https://www.continuum.io/downloads#windows>`_. Here is some `Reddit cheer for Anaconda <https://www.reddit.com/r/Python/comments/3t23vv/what_advantages_are_there_of_using_anaconda/>`_.  Alternatively on OS X, you can use Homebrew to install Python 3.5, virtualenv, virtualenvwrapper, and pip. Alternatively on Linux, you can use apt to install these.

  Update: I hear that using the current Anaconda for Windows and Python 3.4 one can install more of the third-party libraries above than Anaconda for Windows and Python 3.5. In that case, use Python 3.4. It will do for our purposes.

2. Create a directory and virtual environment for your PyClub work. In the virtual environment install the `Jupyter Notebook <https://jupyter.org/>`_. Open a Jupyter notebook.

3. In a Jupyter notebook, write some Python code to solve the following problem, which i took from *Think Python* by Allen B. Downey. "Give me a word with three consecutive double letters. I’ll give you a couple of words that almost qualify, but don’t. For example, the word committee, c-o-m-m-i-t-t-e-e. It would be great except for the ‘i’ that sneaks in there. Or Mississippi: M-i-s-s-i-s-s-i-p-p-i. If you could take out those i’s it would work. But there is a word that has three consecutive pairs of letters and to the best of my knowledge this may be the only word. Of course there are probably 500 more but I can only think of one." Here is a `sufficient wordlist <http://greenteapress.com/thinkpython2/code/words.txt>`_.

4. In a Jupyter notebook, solve the following problem, which i took from *Think Python* by Allen B. Downey. Write a program that reads a list of words and returns a collection of all lists of words that are anagrams of each other, where the collection is sorted from the longest list of anagrams to the shortest list and where the shortest list is of size at least 2.

  Here is an example of what some of the output might look like::

      [
      ['deltas', 'desalt', 'lasted', 'salted', 'slated', 'staled'],
      ['resmelts', 'smelters', 'termless'],
      ['retainers', 'ternaries'],
      ['generating', 'greatening'],
      ]

  Use your function to find all the anagrams in the word list given in problem 3 above. 
  Hint: you might want to build a dictionary that maps a collection of letters to a list of words that can be spelled with those letters.


Homework 2
===========
| Theme: Pandas and GTFS
| Due: 2016-11-15

1. In your PyClub virtual environment install `Pandas <http://pandas.pydata.org/>`_. Complete the Pandas tutorial `here <synesthesiam.com/posts/an-introduction-to-pandas.html>`_, ignoring the first installation step, which you already did. The tutorial uses an older version of Pandas than yours, so some function APIs might have changed. If you encounter errors, check the `Pandas documentation <http://pandas.pydata.org/pandas-docs/stable/>`_ for the current correct usage.

2. Read the `Wikipedia page on GTFS <https://en.wikipedia.org/wiki/GTFS>`_.

3. Download a cleaned version of Auckland's latest GTFS feed from ``data/homework_02``. Working in a Jupyter notebook, complete the following function and test it.

  .. code-block:: python

      def read_gtfs(path):
          """
          Given a path (string or pathlib object) to a (zipped) GTFS feed,
          unzip the feed and save the files to a dictionary whose keys are
          named after GTFS tables ('stops', 'routes', etc.) and whose
          corresponding values are Pandas data frames representing the tables.
          Return the resulting dictionary.

          NOTES:
              - Ignore files that are not valid GTFS; see https://developers.google.com/transit/gtfs/reference/.
              - Ensure that all ID fields that could be strings ('stop_id', 'route_id', etc.) are parsed as strings and not as numbers.    
          """
          pass

  Hint: Use the functions ``shutil.unarchive`` and ``pandas.read_csv`` with the 'dtypes' keyword argument.

4. Using the Auckland GTFS feed and the output of your ``read_gtfs`` function, find the bus route with the longest trip and the length of that trip and find the route with the shortest trip and the length of that trip. By the way, the distances in the Auckland feed are measured in kilometers. 


Homework 3
===========
| Theme: Shapely, GeoJSON, and GTFS
| Due: 2016-11-29

1. In your PyClub virtual environment install Shapely. Then read the 'Introduction' section of the `Shapely user manual  <http://toblerity.org/shapely/manual.html>`_. 

2. Recall your GTFS reader from Homework 2.3, and let us call the output of it a *GTFS feed object*. Implement the following function that converts GTFS shapes to Shapely LineString objects.

  .. code-block:: python

      def shape_to_geometry(feed, shape_id):
          """
          Given a GTFS feed object and a shape ID from that feed, 
          return a Shapely linestring representation of the shape 
          (in WGS84 coordinates, the native coordinate system of GTFS).

          NOTES:
              Raise a ``ValueError`` if ``feed['shapes']`` does not exist or 
              if the shape ID does not exist.
          """
          pass

3. Read the `Wikipedia page on GeoJSON <https://en.wikipedia.org/wiki/GeoJSON>`_. Read also the 'Interoperation' section of the Shapely user manual, and notice that Shapely plays nicely with GeoJSON via the functions  ``shapely.geometry.mapping` and ``shapely.geometry.shape``.

4. Implement the following function that converts GTFS trips to GeoJSON features (as Python dictionaries).

  .. code-block:: python

      def trip_to_geojson(feed, trip_id):
          """
          Given a GTFS feed object and a trip ID from that feed, 
          return a GeoJSON LineString feature (as a Python dictionary) 
          representing the trip's geometry and its metadata 
          (trip ID, direction ID, headsign, etc.).
          Use WGS84 coordinates, the native coordinate system of GTFS.

          NOTES:
              Raise a ``ValueError`` if the appropriate GTFS data does not exist.
          """
          pass

  Hint: Use the function ``shapely.geometry.mapping`` to quickly convert a Shapely geometry into a GeoJSON geometry.

  As a way to test your function's output, convert it to a JSON string via Python's built in ``json.dumps`` function, and then paste that feature collection into `geojson.io <http://geojson.io>`_ as one of the elements in the ``features`` list.

5. Use your functions above to create a simple screen line counter:

  .. code-block:: python

    def compute_screen_line_counts(feed, linestring):
        """
        Find all trips in the given GTFS feed object that intersect the given Shapely LineString 
        (given in WGS84 coordinates), and return a data frame with the columns:

        - ``'trip_id'``
        - ``'route_id'``
        - ``'route_short_name'``
        - ``'direction_id'``
        """
        pass


6. Use your screen line counter to count the number of trips that cross the Auckland Harbour Bridge. Hint: draw your screen line with GeoJSON IO and convert it to a Shapely LineString with the help of the ``shapely.geometry.shape`` function.

  What basic feature(s) is the screen line counter missing to make its output useful to transit analysts?