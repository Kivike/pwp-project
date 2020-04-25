# PWP SPRING 2020
# Game Score API
# Group information
* Student 1. Roope Rajala roope.rajala@student.oulu.fi
* Student 2. Julius Hekkala julius.hekkala@gmail.com
* Student 3. Otto Poikajärvi ottopoikajarvi@gmail.com

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__

## How to setup database

### Dependencies

The requirements.txt file includes all the dependencies. Run `pip install -r requirements.txt` to install the dependencies in a virtual environment.

### Installing the project

Run `pip install -e .` in the project folder in a virtual environment. After that the project works correctly.

### Database version

We are using SQLite 3.28.0

### Create an example populated database for development environment

Example.py in src-folder creates an example populated database. If you run example.py, a database called test.db is created in db-folder.

### Already created example populated database

The same database that example.py creates can be found in the db-folder with the name deliverable2.db

### Create an empty database

Create an empty database with tables created by running `flask init-db` in the root directory of the project.
This is mandatory especially in "production" environment of Flask. 
In "production" environment, the command creates a database file called "gamescores.db" in db-folder.

## Running the application

### Using docker

``` docker build -t pwp:latest . ```

``` docker:run -d -p 5000:5000 pwp ```

### Without docker

Remember to setup the database before running the application.

If you want to run the application, run __in the root directory of the project__:

``` flask run ```

API entry point is ``` http://localhost:5000/api/ ```

For compiling the client, run
``` npm install && npm run build ```

Run environment can be set with FLASK_ENV environmental variable. If the value isn't set, dev mode is used.
Available modes:
- __development__ (database is permanently stored in file db/test.db)
- __production__ (database is permanently stored in file db/gamescores.db)
- __test__ (database is temporarily stored in memory)

To run the app in production mode:
``` FLASK_ENV=live flask run ```



## Frontend workflow
Install depenencies
``` npm install ```

Start webpack bundling process
``` npm run develop ```

## Run the tests

In order to run all the unit tests on the database and resources with coverage reporting, run __in the root directory of the project__:

``` coverage run -m unittest -v && coverage report ```

To run all the unit tests without coverage reporting, run __in the root directory of the project__:

``` python -m unittest -v ```

To just run a single test file, run __in the root directory of the project__:

``` python -m unittest -v test/name_of_file.py```

The resource test files are in test/resource/ directory.

To run a single test function, run __in the root directory of the project__ for example:

``` python -m unittest test.test_player.TestPlayer.testDuplicateIdThrowsError ``` 




