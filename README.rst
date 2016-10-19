PyClub 
*******
This is a repository of supporting material for PyClub, a work-time meetup about Python and data science at MRCagney.


Introduction
=============
- Motivation: Upskill on Python for data science. Python is useful, data science is useful, and the two together are a powerful combination.
- Focus: Tools and processes for analyzing transit and geospatial data, because that's our main work at MRCagney
- Assumption: You have Python proficiency at the level of, say, the `Codeacademy Python2 tutorial <https://www.codecademy.com/learn/python>`_. We will be using Python3, but they're not too different.
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
Theme: Set up and warm up
Due: 2016-11-01

1. On your computer, install Python 3.5, a virtual environment manager, and a Python package manager. You can do all this at once in a straightforward and cross-platform way by installing `Anaconda <https://www.continuum.io/downloads#windows>`_. Here is some `Reddit cheer for Anaconda <https://www.reddit.com/r/Python/comments/3t23vv/what_advantages_are_there_of_using_anaconda/>`_.  Alternatively on OS X, you can use Homebrew to install Python 3.5, virtualenv, virtualenvwrapper, and pip. Alternatively on Linux, you can use apt to install these.

2. Create a directory and virtual environment for your PyClub work. In the virtual environment install the `Jupyter Notebook <https://jupyter.org/>`_. Open a Jupyter notebook.

3. In a Jupyter notebook, write some Python code to solve the following problem, which i took from the *Think Python* book by Allen B. Downey. "Give me a word with three consecutive double letters. I’ll give you a couple of words that almost qualify, but don’t. For example, the word committee, c-o-m-m-i-t-t-e-e. It would be great except for the ‘i’ that sneaks in there. Or Mississippi: M-i-s-s-i-s-s-i-p-p-i. If you could take out those i’s it would work. But there is a word that has three consecutive pairs of letters and to the best of my knowledge this may be the only word. Of course there are probably 500 more but I can only think of one." Here is a `sufficient wordlist <http://greenteapress.com/thinkpython2/code/words.txt>`_.


Homework 2
===========
Theme: Pandas and GTFS
Due: 2016-11-15

1. Read the `Wikipedia page on GTFS <https://en.wikipedia.org/wiki/GTFS>`_. In your PyClub virtual environment install `Pandas <http://pandas.pydata.org/>`_. Download a cleaned version of Auckland's latest GTFS feed from ``data/homework_02``. Working in a Jupyter notebook, complete the following function and test it.

  .. code-block:: python

    def read_gtfs(path):
        """
        Given a path (string or pathlib object) to a (zipped) GTFS feed, unzip the feed and save the files to a dictionary whose keys are named after GTFS tables ('stops', 'routes', etc.) and whose corresponding values are Pandas data frames representing the tables.
        Return the resulting dictionary. 
        """
        pass

  Hint: Use Pandas's ``read_csv`` function.

2. Using the Auckland GTFS feed and the output of your ``read_gtfs`` function, find the route with the longest trip and the length of that trip and find the route with the shortest trip and the length of that trip. By the way, the distances in the Auckland feed are measured in kilometers. 

3. Read the `Wikipedia page on GeoJSON <https://en.wikipedia.org/wiki/GeoJSON>`_. Create a GeoJSON feature collection consisting of two linestrings encoding the shapes of the trips you found above. Cut and paste that feature collection into `geojson.io <http://geojson.io>`_ to visualize the trips. Hint: Create the feature collection as a Python dictionary and then convert it to a JSON string via the ``json.dumps`` function of the ``json`` library (which comes with Python).