# PROJECT SETUP PHASES
## PostgreSQL 14/ pgAdmin4
A database called Getir was installed from scratch. It is very important to
set up this database because most of the operations such as querying data
from the database or importing tables directly to the database through the
sqlalchemy module via pgAdmin4 or Python.
Available in scripts in the `python_related` folder.
## Python/Anaconda
You can find an output of all the modules you will need throughout the
project in a file called requirements.txt. It contains only
Spyder-Kernels and the requirements of this module are redundant. It was
built using Python 3.12.11 and there are no conflicts between modules. The
virtual environment created for this project from scratch was installed with
Anaconda and Conda version 23.9.0 was used.
## QGIS
QGIS version 3.30.0-'s-Hertogenbosch was used throughout the project. No
crashes were encountered during the study despite the peak hours. WGS84
(EPSG:4326) coordinate system was used for all data containing coordinates.
No extra plugin is required. The PostgreSQL fetch database must be
registered to QGIS via Data Source Manager. This step is important for
frequent use in the project, as well as for closing and reopening the
project without any problems.
## SQL scripts
These files can be accessed from the Get/SQL related folder. In the first
step run `/getir/python_related/ push.py` file and import both order and
warehouse CSV files to postgreSQL system. After the transfer, the script
`/getir/sql_related/getir_create_geom.sql` is followed step by step. Run
`/getir/python_related/getir_data.py`. If you are going to generate the
bursa_district.geojson file that you will find in the file yourself using
OSM, you must convert it to Multipolygon type, for this, the process at the
bottom of the script is applied, but before that, you need to delete the
"@relations" column in the geojson file you obtained via OSM. This problem
is overcome by using Geopandas or QGIS. If all goes smoothly, the Geojson
output is imported into the PostgreSQL database. After completion
The script `/sql_related/py/get_dist.sql` needs to be followed.
The `./get_query.sql` file is the file that contains the queries made while
generating the data. Although it is only a query file, not using it does not
cause any problems. Executing the code blocks in the SQL files one by one
will prevent possible errors.
## Python Scripts
- At this stage, it is difficult to categorize transactions under a
certain heading because will be used all together.
Run the script `/python_related/get_service_ors.py`. I should mention
that the OpenRouteService (ORS) API key required for route calculation
on Heigit is mandatory for those who plan to generate data. The key
requires the creation of an .env file under the `/getir/python_related/`
folder (ORS_API_KEY=your_key_here) or you can paste your own key. Every 24
hours your query limits are renewed according to query types. There was
no limit exceeding in the creation of the whole project. Only the
geojson file generated with the script must be imported to PostgreSQL,
all other files are imported automatically. The project does not
require to open any CSVs from QGIS, one time **provided that the output
in geojson format is imported into PostgreSQL**.
- From the same folder, `get_service_ors_bicycle.py` is executed
and the same process is performed according to the bicycle
scenario, the geojson output must be exported to PostgreSQL.
- `ors.compare.py` creates a table showing which of the two different
vehicle scenarios is advantageous according to time and distance. The
CSV generated at the end of the script is optional, not mandatory.
- `pipe.py` is an extra script where you can run your own
SQL queries and convert them into a DataFrame.
- `shortest.py` is the distance between two pairs of coordinates and the
time
a simple extra script that you can calculate.
- `service_point_needed.py`, which is the output of "fetch_service_ors.py"
Using the points in `sip_war_with_routes.csv` file, the script outputs
geojson as a result of the process using Kmeans according to the number
of the desired service point.
- `service_point_isochrone[median,min,half_median].py` scripts ORS
is used to create isochrome maps. The purpose of creating different
scripts is to obtain different maps according to different statistical
data obtained from "delivery_duration", i.e. delivery time. You can
work with all of them or with the one you prefer, or even not at all.
- `siparis_bursa_valid.py` combines the "siparis" table and
"bursa_mahalle_valid" tables in PostgreSQL and saves them in geojson
format. The extra script does not contribute to the following stages.
- `neighborhood_order_count.py` A script that combines two different
PostgreSQL queries to show the total number of orders based on
neighborhoods on QGIS and produces "order_counts_by_hood.geojson"
output.
- `district_order_count.py` Runs a PostgreSQL query to generate district
based order count and saves the output as
"district_order_count.geojson".
- `gen_df_then_to_postgre` Neighborhood-based population information has
been the most difficult data to obtain in this project, not only
accessing the data, but also editing CSV files created non-standard
after accessing the current data, capturing minor changes that may
occur in the neighborhood names after editing, and runs the PostgreSQL
query that ensures that they are assigned to the correct neighborhoods.
After the query
The `neighborhood_pop_matched.geojson` file contains the associated
neighborhood population values and neighborhood regions.

## Results

Orders were attached to their corresponding storage locations with respect to the minimum distance that is calculated by iterating for every storage. 

![sip_density](https://github.com/Zodijackyl98/getir_analysis/blob/main/Stats/spatial/density_sip_points.png)

To find optimum service points, clustering method was used and the solution with 4 service points is shown below.

![service_points](https://github.com/Zodijackyl98/getir_analysis/blob/main/Stats/spatial/service_points_4.png)

Relationship between area and the number of order for every neighbourhood also brings us useful information. 

![order_density](https://github.com/Zodijackyl98/getir_analysis/blob/main/Stats/spatial/order_density_per_hood.png)

Analyzing real-life delivery route simulation and calculating delivery time accordingly with different type of vehicles helps choosing which one is better at which under different order, storage and service points locations and then creating table to decide which one we should choose; the route that we can save time by using a car but by doing that risking consuming more fuel but gaining opportunity to carry more items or the route that we can save fuel but arriving late to costumers.

![car_bike_routes](https://github.com/Zodijackyl98/getir_analysis/blob/main/Stats/spatial/car_bike_routes_wh5.png)

![car_bike_routes](https://github.com/Zodijackyl98/getir_analysis/blob/main/Stats/routes_better.png)

With the help of ısochrone maps, one can combine it with clustering method and optimize both service point number and service point location decision making process easily.

![car_bike_routes](https://github.com/Zodijackyl98/getir_analysis/blob/main/Stats/spatial/isochrone_service_problem.png)




## Django Support 
### Information
 - Django support added with the V1.1.0 update is an extra feature and does not affect those using the base V1.0.0 version.
### Instructions
 - All Django files related to the project can be found in the `/get/Django` folder. 
 - It is necessary to create the id information required for Django to
work properly, which can be found in the `updates_for_django.sql` file.
- To install Python Django and psycopg modules
is needed. - In `settings.py`, the DB with the same name and password used
in the project has been added by default and necessary arrangements have
been made for TEMPLATES and INSTALLED_APPS.
 - `models.py` file was created
automatically with `python manage.py inspectdb > analytics/models.py`
command and all tables in PostgreSQL are included.
 - `views.py` The logic of
the 3 tables selected as examples and the main page, the URLs to which they
are linked and all filtering operations are defined here.
 - `admin.py` After
a superuser is created, 3 tables are added to the admin window as an
example. For admin login, it can be accessed from `admin/` or access can be
provided from the top right from the homepage of the site.
 - When conditions are met
The development server can be started by running `python manage.py
runserver`.
 - Currently added URL structures are; `/home, /orders, /sip-per-capita and /sip-density-per-hood`.