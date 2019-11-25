PyClub
*******
This is a repository of supporting material for PyClub, a work-time meetup about Python and data analysis at MRCagney.


Introduction
=============
- Motivation: Upskill on Python for data analysis. Python is useful, data analysis is useful, and the two together are a powerful combination.

- Focus: Tools and processes for analyzing transit and geospatial data, because that's our main work at MRCagney

- Assumption: You are proficient in Python at the level of, say, the `Codeacademy Python 2 tutorial <https://www.codecademy.com/learn/python>`_. We will be using Python 3, but they're not too different.

- Third-party Python libraries that we will use a lot:

  * NumPy for numerical computing
  * Pandas for tabular data
  * Shapely and Fiona for geospatial data
  * Geopandas, which combines Shapely with Pandas
  * GTFS Kit for GTFS feeds

- Other notable third-party Python libraries for data analysis:

  * SciPy for scientific/engineering computing
  * Statsmodels for statistical modeling
  * Scikit-Learn for machine learning
  * Requests for API calls
  * Scrapy for web crawling and scraping
  * Python-Highcharts for plotting


Homework 1
===========
Theme: Set up and warm up

1. On your computer, install Python 3.7, a virtual environment manager, and a Python package manager. You can do all this at once in a straightforward and cross-platform way by installing `Anaconda <https://www.continuum.io/downloads#windows>`_. Here is some `Reddit cheer for Anaconda <https://www.reddit.com/r/Python/comments/3t23vv/what_advantages_are_there_of_using_anaconda/>`_.  Alternatively on OS X, you can use Homebrew to install Python 3.7, virtualenv, virtualenvwrapper, and poetry. Alternatively on Linux, you can use apt to install these.

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
Theme: Tabular data and GTFS

1. In your PyClub virtual environment install `Pandas <http://pandas.pydata.org/>`_. Complete the Pandas tutorial `here <synesthesiam.com/posts/an-introduction-to-pandas.html>`_, ignoring the first installation step, which you already did. The tutorial uses an older version of Pandas than yours, so some function APIs might have changed. If you encounter errors, check the `Pandas documentation <http://pandas.pydata.org/pandas-docs/stable/>`_ for the current correct usage.

2. Read the `Wikipedia page on GTFS <https://en.wikipedia.org/wiki/GTFS>`_, and for more information see the `GTFS reference <https://developers.google.com/transit/gtfs/>`_.

3. Consider the Auckland GTFS feed ``data/auckland_gtfs_20190524.zip``. Working in a Jupyter notebook, complete the following function and test it.

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

   Hint: Use the functions ``shutil.unpack_archive`` and ``pandas.read_csv`` with the 'dtypes' keyword argument.

4. Using the Auckland GTFS feed and the output of your ``read_gtfs`` function, find the bus route with the longest trip and the length of that trip and find the route with the shortest trip and the length of that trip. By the way, the distances in the Auckland feed are measured in kilometers.


Homework 3
===========
Theme: Geodata

1. In your PyClub virtual environment install Shapely. Then read the 'Introduction' section of the `Shapely user manual  <http://toblerity.org/shapely/manual.html>`_.

2. Recall your GTFS reader from Homework 2.3, and let us call the output of it a *GTFS feed object*. Implement the following function that converts GTFS shapes to Shapely LineString objects.

   .. code-block:: python

      def build_geometry_by_shape(feed, shape_ids=None):
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

   Hint: Use the function ``shapely.geometry.mapping`` to quickly convert a Shapely geometry into a GeoJSON geometry. Also, replace ``numpy.nan`` data values with a string such as ``'n/a'`` to avoid hassles when dumping to JSON.

   As a way to test your function's output, convert it to a JSON string via Python's built in ``json.dumps`` function, and then paste that feature collection into `geojson.io <http://geojson.io>`_ as one of the elements in the ``features`` list. You can also test your output at `GeoJSONLint <http://geojsonlint.com/>`_.

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

   What basic feature(s) is the screen line counter missing to make its output useful to transit analysts? How could you speed up your function?


Homework 4
===========
Theme: Source code control

This homework assignment is not about data analysis per se, but understanding the content herein ---version control in general and Git in particular--- will help you tremendously on all your data analysis and programming projects.

1. Read the beginning of the `Wikipedia article on Git <https://en.wikipedia.org/wiki/Git>`_. Read `this conceptual Git tutorial <https://www.sbf5.com/~cduan/technical/git/>`_. Do `this interactive, command-driven Git tutorial <https://try.github.io/levels/1/challenges/1>`_. For more practice, work through `these Lyndia tutorials <https://www.lynda.com/Git-tutorials/Git-Essential-Training/100222-2.html>`_.

2. Initialize a Git repository in your PyClub directory and use Git from now on to track its changes.

3. If you work on PyClub on more than one computer or on a team, create a Github account (free public repositories) or a Gitlab account (free public *and* private repositories) to host your PyClub Git repository on the web. Practice syncing your local Git repository with this remote Git repository.  You might also want to read `this tutorial on collaborative Git workflows <https://www.atlassian.com/git/tutorials/comparing-workflows>`_.


Homework 5
===========
Theme: Geodata again

1. `Read about GeoPandas <http://geopandas.org/index.html>`_ and then `install it <http://geopandas.org/install.html>`_.

2. Create a GeoPandas geodataframe of Auckland roads from the appropriate file in the ``data`` directory. I got this data from `Mapzen metro extracts IMPOSM format here <https://mapzen.com/data/metro-extracts/metro/auckland_new-zealand/>`_.  Reproject the data from the WGS84 projection (EPSG 4326) to New Zealand Transvere Mercator projection (EPSG 2193) so that the units will be meters.

3. Create a GeoPandas geodataframe of New Zealand crash point locations from the appropriate file in the ``data`` directory. I got this data from `NZTA <http://www.nzta.govt.nz/safety/safety-resources/road-safety-information-and-tools/disaggregated-crash-data/>`_.  Set the project for the geodataframe to the New Zealand Transvere Mercator projection (EPSG 2193). Restrict the crashes to Auckland locations.

4. Plot the crashes overlaid on the roads in your notebook.

5. Compute Auckland's crashy roads. Do this by scoring each road according to the sum of its number of crashes divided by its length in meters.

   Hint: Buffer the crash points by 10 meters, say, and spatially join them with the roads.
   Aggregate the result to calculate the crash score for each road.

6. Plot the result using GeoJSON IO, color-coding the roads by crash score.

   Hint: Add to your geodataframe from step 5 the extra columns "stroke" (line color as a HEX color code) and "stroke-width" (line weight in number of pixels) and then export to GeoJSON. Using the `Spectra library <https://github.com/jsvine/spectra>`_, say, to smoothly blend colors is a nice extra touch.


Homework 6
===========
Theme: Web APIs

1. Read about HTTP requests and the Requests library, and then install Requests.

2. Play with the `Mapzen isochrone API <https://mapzen.com/documentation/mobility/isochrone/api-reference/>`_ enough to issue a successful GET request. You'll need a Mapzen API key for this, which you can `get from Mapzen here <https://mapzen.com/documentation/mobility/isochrone/api-reference/>`_, if you have a Github account, or you can use my API key, which you can get from me in person. Heed the `rate limits <https://mapzen.com/documentation/overview/#mapzen-isochrone>`_ on the isochrone API.

3. Extract all the train stations from the Auckland GTFS feed in the ``data`` directory.

   Hint: Look for the word 'Train' in the ``stop_name`` column.

4. For each train station, compute its 1 km walking catchment (as a polygon) using the Mapzen isochrone API. Because the API only accepts time limits and not distance limits, we have to approximate this computation by choosing an appropriate walking speed and time limit to imitate a 1 km distance limit, e.g. 1 km/h and 60 minutes. Additionally for each train station compute its 1 km flying catchment (as a polygon, which will be a circle around the station of radius 1 km).

   Hint: For the flying catchments, you can use GeoPandas, the NZTM projection (EPSG 2193), and the ``buffer`` function.

5. For each train station, compute the ratio of its walking catchment area to its flying catchment area.

6. Plot the flying catchments, walking catchments, and train stations (in that order) using GeoJSON IO, color-coding the walking catchments by area ratio.

   Hint: Add to your geodataframe of walking catchments the extra columns "fill" (HEX color code) and "fill-opacity" (float between 0 (clear) to 1 (opaque)) and then export to GeoJSON. Using the `Spectra library <https://github.com/jsvine/spectra>`_, say, to smoothly blend colors is a nice extra touch.

7. Is the area ratio above a good measure of walking accessibility of the train stations? Discuss, and discuss other measures.


Homework 7
============
Theme: Plotting

1. There are *heaps* of plotting libraries for Python, but let's focus on just two good open-source one:

   - `Plotnine <https://github.com/has2k1/plotnine>`_. Static plots using grammar of graphics syntax with an API similar to ggplot2 for R.
   - `Plotly.py <https://github.com/plotly/plotly.py>`_. Interactive plots using declarative syntax. Also links to Plot.ly for sharing and collaborating on plots on the web.

2. Install Plotnine and make some plots.
3. Install the Plotly.py and make the same plots.
4. What are some of the strengths and weaknesses of Plotnine and Plotly.py?
5. Extra credit: `try Cufflinks <https://plot.ly/python/v3/ipython-notebooks/cufflinks/>`_, which binds Plotly directly to Pandas dataframes.


Homework 8
===========
Theme: Automated testing

1. Read the `this introduction to automated testing in Python <https://jeffknupp.com/blog/2013/12/09/improve-your-python-understanding-unit-testing/>`_, then read the good tips at the beginning of `the Python Guide section on testing <https://python-guide-pt-br.readthedocs.io/en/latest/writing/tests/>`_.

2. Read `the getting started section of pytest <https://docs.pytest.org/en/latest/getting-started.html>`_ and install pytest.

3. Using pytest, write some automated tests for a project you've been working on. Where to put these tests?  Follow `the Python Guide advice on structuring your project <https://python-guide-pt-br.readthedocs.io/en/latest/writing/structure/>`_.


Homework 9
===========
Theme: Object-oriented programming

1. Read about object-oriented programming (OOP) in Python. Start with `this short tutorial <https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/>`_.  Then, as time permits, dig deeper by reading `this tutorial chapter <http://www.python-course.eu/python3_object_oriented_programming.php>`_ and the subsequent chapters up to and including "Metaclass Use Case".

2. Rewrite your GTFS utilities from Homeworks 2 & 3 in an object-oriented way. In particular, create a Feed class to represent GTFS feeds, convert your feed functions into Feed methods, and rewrite the function ``read_gtfs()`` to output a Feed instance.


Homework 10
===========
Theme: Creating a Python package

1. If you have not done so already, read the section of the Hitchhiker's Guide to Python on `writing great Python code <http://docs.python-guide.org/en/latest/#writing-great-python-code>`_.

2. Following the guide's advice, create your own Python package for a project you are working on or for the GTFS toolkit we have been developing. Be sure to include a README file, a license, docstrings, automated tests, and a ``setup.py`` file. For extra credit, `use Sphinx to build your project documentation <http://docs.python-guide.org/en/latest/writing/documentation/#sphinx>`_.  Of course, you should be doing this all within a Git repository.

3. Learn how to make your project installable with pip by following `these instructions <http://peterdowns.com/posts/first-time-with-pypi.html>`_.  Go through the motions and publish to the PyPi test server at least.  If really want to share your project with the world, then publish it to the PyPi live server afterwards.


Homework 11
============
Theme: Dash

1. Read about `Dash <https://plot.ly/dash/>`_, a Python library for building analytical web applications without JavaScript, and complete the Dash tutorial (on the same page linked to above). It helps to know the basics of HTML and CSS, which `Code Academy has a nice tutorial for<https://www.codecademy.com/ar/tracks/htmlcss>`_.

2. Build a Dash app that runs on your local machine. We'll talk about deploying to a web server later.


Resources
==========
- `The Hitchhiker's Guide to Python <http://docs.python-guide.org/en/latest/>`_
- `PEP8 <http://pep8.org/>`_
