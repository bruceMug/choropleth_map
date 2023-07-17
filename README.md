# Documentation
## Project title: Choropleth Map Visualization with python, PostgreSQL and D3.js

The goal of this project is to create a web application that leverages PostgreSQL as a database to store geographical data and D3.js library to generate a choropleth map visualization based on the pm2_5. The choropleth map will display the distribution of PM2.5 across different parishes in Uganda.

## Table of contents
[About the project](#about-the-project)
[Getting started (installation and usage)](#getting-started-installation-and-usage)
[Packages and modules](#packages-and-modules)
[Design decisions](#design-decisions)
 - [Architecture](#architecture)
 - [Technologies/frameworks/libraries](#technologiesframeworkslibraries)
 - [Performance and scalability](#performance-and-scalability)
 - [Security](#security)
[Deployment](#deployment)
[Contributing](#contributing)
[License](#license)


## About the project



## Getting started (installation and usage)
To get a local copy up and running follow these simple steps.
1. Clone the repo

```git clone https://github.com/brucemug/choropleth_map.git```
2. Navigate to the project directory
```cd choropleth_map```
3. Create a virtual environment
```python3 -m venv venv```
4. Activate the virtual environment

```source venv/bin/activate``` or ```venv\Scripts\activate``` (windows)
5. Install the required packages
```pip install -r requirements.txt```
6. Create a .env file and add the following variables:

```DB_NAME=<database name>```
```DB_USER=<database user>```
```DB_PASSWORD=<database password>```
```DB_HOST=<database host>```
```DB_PORT=<database port>```
7. Run the app
```python app.py``` or ```flask run```
8. Open the browser and navigate to ```http://localhost:5000``` or ```http://127.0.0.1:5000```


## Packages and modules
The following packages and modules are required to run the project:
- python 3.11.2
This can be installed using the following command:
```sudo apt-get install python3.11.2```

- postgresql-15.3-2
This can be installed from the official website: https://www.postgresql.org/download/windows/. Further the postgis bundle can be got from the following link: https://postgis.net/install/ . The postgis bundle contains the postgis extension which is needed to read the geographical data.

- Flask 2.3.2
This can be installed using ```pip install flask```

- psycopg2 2.9.6
This can be installed using ```pip install psycopg2``` .For connection to the database and querying the data.

- shapely 2.0.1
This can be installed using ```pip install shapely``` .For converting wkb to geometry coordinates.

- redis 7.0.12
This can be installed from the official website: https://redis.io/download

- python-dotenv 1.0.0
This can be installed using the following command:
```pip install python-dotenv```

- d3.js
Apply the following CDN to your html file:

```<script src="https://d3js.org/d3.v4.js"></script>```

```<script src="https://d3js.org/d3-geo-projection.v2.min.js"></script>```




## Design decisions
### Architecture
The project is designed using the client-server architecture where the client is the web browser and the server is the web server. The client and server communicate over the internet using HTTP protocol. The client sends a request to the server and the server responds with the requested data. The client is responsible for displaying the data to the user. The server is responsible for processing the request and sending the response to the client. The client and server communicate using JSON format.



### Technologies/frameworks/libraries
I used the following technologies/frameworks/libraries to implement the project:
- Python
- PostgreSQL
- PostGIS
- Flask, D3.js
I used the flask framework to create the web server and also generate a feature collection that was passed to d3.js to generate the choropleth map visualization.


I used the postgre database to store the data that was needed for the project. The size of the data amounted to ~1GB. I used the postgis extension to read the geographical data. Within the code, I used the psycopg2 library to connect to the database and query the data and a shapely library to convert the data to geojson format which is the format that is used by the D3.js library to generate the choropleth map visualization.


### Performance and scalability
During the development of the project, a mere execution of the code took a lot of time. forexample fetching and visualizing the data for 1000 parishes took about one minute. Small as it looks, this was a lot of time for the user to wait for the data to be fetched and visualized. Also imagine! what it would take for 10000 parishes.
Different techniques had to be employed.


First, I refactored the code to improve performance and scalability for example using the ```timeit``` module to measure the time it took for parts of the code to execute. I did this to identify the parts of the code that were taking a lot of time to execute. I then refactored by changing the following parts of the code:

from 
```
features = []
    i = 0
    for row in rows:
        if i < 1000:
            parish = row[0]
            pm2_5 = row[1]
            geometry = row[2]
            i = i+1
            features.append(to_geojson(parish, round(pm2_5), geometry, id=i))
```

to (list comprehension technique)
```
features = [ to_geojson(row[0], round(row[1]), row[2], id=i) for i, row in enumerate(rows) if i < 10000 ]
``` 


I also ensured the precompiling of the wkb loading function (```load_wkb = wkb.loads```) happened once instead of every time the function was called by moving the function outside the ```togeojson``` function.
This (comprehension and precompiling) improved performance by ~ 10 seconds.


Secondly, I used parallel processing to improve performance. I used the ```concurrent.features``` module to create a pool of processes that would execute the code in parallel. I used the ```map``` method to map the function to the pool of processes. This didn't quite improve performance as expected.

I employed the use of generator objects to try to progressively fetch data from the database. I used the ```yield``` keyword to create a generator object. I then used the ```next()``` function to fetch the next row from the database. This didn't quite work as expected since the data was still fetched from the database at once. 
Though ```yield```  wasn't helpful, it was a great learning experience and the keyword can come in handy when returning multiple times from a function rather than the conventional return statement.

More about ```yield``` can be found here: https://www.programiz.com/python-programming/generator and here: [www.simplilearn.com/yield](https://www.simplilearn.com/tutorials/python-tutorial/yield-in-python#:~:text=The%20Yield%20keyword%20in%20Python%20is%20similar%20to%20a%20return,of%20simply%20returning%20a%20value)

Next, I needed a solution in which the data was fetched and visualized in chunks.This would work in that only a certain number of rows are fetched from the database, converted to feature collection and then send to d3.js for visualization before another x rows are fetched. I used the global offset variable to keep track of the number of rows that had been fetched. I then used a custom ```fetchandRenderMap()``` function plus ```(`/map?offset=${offset}`)``` in js to achieve the feat. This had been a problem since that start i.e (progressively render the map as the data is fetched from the database).

Lastly, I used redis for caching. I used the ```redis``` library to connect to the redis server. I then used the ```set``` method to set the key-value pair in the redis server. I then used the ```get``` method to get the value from the redis server.


### Security
I used the following techniques to improve security: Instead of having the database credentials embedded with in the code, I created a .env file and stored the credentials in the .env file. I then used the python-dotenv library to load the credentials from the .env file through the config.py file. I then imported the config.py file in the app.py file and used the credentials to connect to the database.


## Deployment

## Contributing
To contribute to this project, please read the [contributing guidelines](CONTRIBUTING.md).

## License
This project is licensed under the [MIT License](LICENSE).