PRACTICAL_LIST
==============
[Practical 1: Analyze impact of index , type of index on query performance](practical_1/practical_1.pdf)

[Practical 2: Analyze impact of storage format](practical_2/practical_2.pdf)

[Practical 3: Implementation of B+ Tree](practical_3/practical3.pdf)

[Practical 4: Extendsible Hashing](practical_4/practical_4.pdf)

[Practical 5: Linear Hashing](practical_5/doc/practical_5.pdf)

[Practical 6: Iterator for selection and Join](practical_6/doc/practical_6.pdf)

[Practical 7: Implementation of sorting based two pass algorithm](practical_7/doc/practical_7.pdf)

[Practical 9: Query optimization](practical_9/doc/practical9.pdf)

[Practical 10: Concurrency Scenario](practical_10/doc/practical_10.pdf)



INITIAL CONFIGURATION
=====================
### Step 1:
Installation prerequisite
- Python
- Virtual env
- activate virtual env
- mysql
- python [mysqlclient](https://pypi.org/project/mysqlclient/)

also you might need to install

    $ sudo apt-get install libmysqlclient-dev

before running below command

    pip install mysqlclient

### Step 2: Install Project requirements

    pip install -r requirements.txt

### Step 3: Create Database

    create database ds_lab CHARACTER SET utf8 COLLATE utf8_general_ci;

### Step 4: Migration

    python manage.py migrate

### Step 5: Generating data

    python manage.py adddummy 10000
