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

### Database version

We are using SQLite 3.28.0

### Create an example populated database

Example.py in src-folder creates an example populated database. To run that, run __in the root directory of the project__: 

``` python -m src.example```

A database called test.db is created in db-folder.

### Already created example populated database

The same database that example.py creates can be found in the db-folder with the name deliverable2.db

### Test running the application

If you want to test running the application (well, there is no functionality yet obviously), run __in the root directory of the project__:

``` python -m flask run ```

### Run the tests on the database

In order to run all the unit tests on the database, run __in the root directory of the project__:

``` python -m unittest ```

To run a single test file, run __in the root directory of the project__:

``` python -m unittest test.name_of_file_without_py ```

To run a single test function, run __in the root directory of the project__ for example:

``` python -m unittest test.test_player.TestPlayer.testDuplicateIdThrowsError ``` 




