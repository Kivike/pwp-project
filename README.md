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

Run `pip install - e .` in the project folder in a virtual environment. After that the project works correctly.

### Database version

We are using SQLite 3.28.0

### Create an example populated database

Example.py in src-folder creates an example populated database. If you run example.py, a database called test.db is created in db-folder.

### Already created example populated database

The same database that example.py creates can be found in the db-folder with the name deliverable2.db


### Running the application

If you want to run the application, run __in the root directory of the project__:

``` flask run ```

Run environment can be set with FLASK_ENV environmental variable. If the value isn't set, dev mode is used.
Available modes:
- __development__ (database is permanently stored in file db/test.db)
- __production__ (database is permanently stored in file db/gamescores.db)
- __test__ (database is temporarily stored in memory)

To run the app in production mode:
``` FLASK_ENV=live flask run ```

### Run the tests on the database

In order to run all the unit tests on the database with coverage reporting, run __in the root directory of the project__:

``` coverage run -m unittest -v && coverage report ```

To run all the unit tests without coverage reporting, run __in the root directory of the project__:

``` python -m unittest -v ```

To just run a single test file, run __in the root directory of the project__:

``` python -m unittest -v test/name_of_file.py```

To run a single test function, run __in the root directory of the project__ for example:

``` python -m unittest test.test_player.TestPlayer.testDuplicateIdThrowsError ``` 




