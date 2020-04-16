# Meetings notes

## Meeting 1.
* **DATE:** 13.2.2020
* **ASSISTANTS:** Mika Oja

### Minutes
Overall the structure of the database seemed clear. Mika commented that "GameType" could be rather called "GameTitle" but since the GameType model involves other information in addition to the title we determined that changing that name would not be necessary. There had been some confusion related to what a resource is, but it was cleared up in the discussion. That is why we had planned so many models (well, we ended up cutting Permission). It was discussed that creating instances of e.g. games should be done via collections. Also it was discussed that token authentication could be used that is in each request. 
There was some discussion about having an abstract resource "teams" that players could be a part of - this will most probably not be implemented during the course. The use of leaderboards was discussed a bit as well, they should be used during api calls so sorting is easier. 

### Action points
No immediate action in relation to deliverable 1 was deemed necessary. 

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 2.
* **DATE:** 24.2.2020
* **ASSISTANTS:** Mika Oja

### Minutes
The amount of tables in the project currently is enough. The foreign keys were not defined correctly, namely the deletion was not defined correctly in the relationships. All the foreign keys' on_delete behavior should be explicitly defined. Also, there were some mistakes in the tables, where on_delete behavior was "SET NULL" but the foreign keys were not nullable.

The unit tests were otherwise comprehensive, but there were no tests related to deleting items. Also, there should be information about the performed unit tests in the output. There should be a coverage report for the tests in the output.

Also, it was discussed that no API calls should be done with database IDs. So, there should be separate "IDs" for the API calls.  

### Action points

1. Fix the on_delete behavior of the foreign keys in the tables. Define all on_delete behaviors of foreign keys explicitly. Add the behavior to the relationship.
2. Fix the foreign keys that had "SET NULL" as on_delete behavior and were also not nullable.
3. Add unit tests that test the deletion of items.
4. Add more information about the performed tests in the output, there should be a coverage report.
5. Add "IDs" that are used for API calls to tables where they are needed.


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 3.
* **DATE:** 17.3.2020
* **ASSISTANTS:** Mika Oja

### Minutes
There are quite a lot of resources currently. Only part (at least 6) of them have to be implemented. We have to decide what will be implemented and what will be left not implemented. 

In the state diagram, there was a disconnection between the left and the right side of the diagram. An "up" link should be added to Game scoreboard. Also, Tournament, Player and Game collections should have links between them to help the user move on collection level. There should also be a link from Game back to Tournament, which did not exist at the time of the meeting. Otherwise, the diagram looked quite alright.

Apiary documentation looks okay. 

### Action points

1. Add new links to the API. Add an "up" link from Game scoreboard to Game. Add links between Tournament, Player and Game collections. Add a link from Game back to Tournament.

### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Meeting 4.
* **DATE:** 15.4.2020
* **ASSISTANTS:** Iván Sánchez Milara

### Minutes
In router.py there should be a comment about leaderboard and tournament resources not being implemented for clarity. To get full points for the deliverable, more comments are needed in tests as well as some in the resource files. 

We encountered one instance during the meeting where the documentation in Apiary did not completely match the implementation. The documentation in Apiary should be checked for mistakes. 

Overall, the situation with the implementation is good. 

### Action points

1. Check Apiary documentation for impactful mistakes. 
2. Comment in router.py that leaderboard and tournament resources are not implemented. If we have time, more comments in tests and resource files. 


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Midterm meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

## Final meeting
* **DATE:**
* **ASSISTANTS:**

### Minutes
*Summary of what was discussed during the meeting*

### Action points
*List here the actions points discussed with assistants*


### Comments from staff
*ONLY USED BY COURSE STAFF: Additional comments from the course staff*

