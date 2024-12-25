# Data Engineering demo project.

### Process steps:
* Scrap currency ratings from [Priorbank web page](https://www.prior.by/web/).
* Upload it into PostgreSQL database.
* Display ratings history on [Gnrafana dashboard.](https://leotepl.grafana.net/public-dashboards/f614b30a1e7549ae806a9f9fe6398396)

### Skills used:
* ETL: The process to extract data from web page transform and load it to PostgreSQL datatbase is implemented as GitHub action.
* Web scrapping: selenium, BeautifulSoup.
* Python: selenium, BeautifulSoup, lxml, pandas, psycopg2,  regular expressions.
* Data modeling: pgmodeler.
* PosgreSQL server administration: pgadmin.
* Data analysis: SQL.
* Data visualizaton: Grafana.

## Process outline.
The process has two branches.
1. Load currency ratings data to PostgreSQL database on my laptop.
2. Load currency ratings data to PostgreSQL database on the cloud ([Neon](https://neon.tech/)). Visualize data on Grafana dashboard with PostgreSQL on Neon as datasource.

## GitHub 
Github action runs periodically by the schedule.
* Step 1. Python script runs java with selenium and saves raw web page in the file.
* Step 2. (For branch 2). Python script processes the page taken from the file and extracts currency rating data into pandas dataframe. The dataframe is loaded to PostgreSQL database on Neon.
* Step 3. (For branch 1). The raw web file is commited to GitHub master branch.

 ## My laptop
 * Step 1. Python script is run by chron to pull raw html files from GitHub to local git repository.
 * Step 2. Same processing as on branch 2 is done on each html file to load data into PostgreSQL database on laptop.
 * Step 3. The processed html files are gzipped and saved to local history folder.
 * Step 4. The processed html files are deleted and this deletion is commited to GitHub.

 ## Grafana on cloud
 Periodically refreshes data on the dashboard panels by running SQL queries to extract specific currency exchange/conversion ratings. 

## Q&A
Q: Why GitHub action?  
A: I could not find another free cloud resource to run this process.   

 ## Todo:
Provide more details about database design and source code components.
