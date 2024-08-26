Visualization of some Census 2021 data relative to the City of Toronto Neighbourhood maps. Project ongoing and is a work in progress.

* `census.py` is relative to transportation data in Ward 23 and generates a bar graph
* `census2.py` is the same but City-wide
* `maptest.py` generates a map of just the biking data city wide

To start, download all of the files and install Python. On command line install the needed packages
* **Plotly**: `pip install plotly`
* **Geopandas**: `pip install geopandas`
* **Pandas** (non geojson): `pip install pandas`
* **JSON interpreter**: `pip install json`
* **Dash**: `pip install dash`

Then simply run `py [name].py`. For example, if you wanted to run `maptest.py` then on your command prompt run `py maptest.py`.

Data sourced from Toronto's Open Data repository:
* Neighbourhood census data sourced from: https://open.toronto.ca/dataset/neighbourhood-profiles
* Neighbourhood boundaries sourced from: https://open.toronto.ca/dataset/neighbourhoods

Enjoy! 
