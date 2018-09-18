Practical 1
===========
> a) Import Database, understand Query execution plan using SQL Yog  
> b) Analyze impact of index , type of index on query performance

a) Database Structure
---------------------
- Database: **MySQL**  
- Total data rows in table ds_leaderboard: **4,00,000**
- PC Configuration  
    : Intel® Core™ i3-4130 CPU @ 3.40GHz × 4  
    : ~4 GB RAM

**ds_leaderboard**

    CREATE TABLE `ds_leaderboard` ( 
        `id` Int( 11 ) AUTO_INCREMENT NOT NULL,
        `name` VarChar( 64 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        `email` VarChar( 254 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        `organizer` VarChar( 256 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        `score` Double( 22, 0 ) NOT NULL,
        `time` VarChar( 16 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        `country` VarChar( 128 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        `language_id` Int( 11 ) NULL,
        PRIMARY KEY ( `id` ) )
    CHARACTER SET = utf8
    COLLATE = utf8_general_ci
    ENGINE = InnoDB
    AUTO_INCREMENT = 400001;
-- -------------------------------------------------------------
**ds_programminglanguage**

    CREATE TABLE `ds_programminglanguage` ( 
        `id` Int( 11 ) AUTO_INCREMENT NOT NULL,
        `name` VarChar( 32 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
        `version` VarChar( 16 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
        `release` Date NULL,
        PRIMARY KEY ( `id` ) )
    CHARACTER SET = utf8
    COLLATE = utf8_general_ci
    ENGINE = InnoDB
    AUTO_INCREMENT = 13;
-- -------------------------------------------------------------

b) Impact of index
------------------
### Query

    select * from ds_leaderboard;
Query time: 1.947 s  
Index used : No index to be used because we are loading all data of all attribute(column)

### Query

    select * from ds_leaderboard where language_id=1;
Query time: 235 ms  
No. of records: 33243  
Index used : index on attribute language_id  

### Query

    select * from ds_leaderboard ignore index(pl) where language_id=1;
Query time: 287 ms  
No. of records: 33243  
Index used : (No index) ignoring index on attribute language_id  

### Query

    select name,language_id from ds_leaderboard where language_id between 1 and 5;
Query time: 226 ms  
No. of records: 166490  
Index used : (No index used) (possible key on language_id)  


### Query

    select name,language_id from ds_leaderboard use index(pl) where language_id between 1 and 5;

|  |  |
|---|---|
| Query time | 206 ms |  
| No. of records | 166490 |  
| Index used | forced to use index on language_id |  


### Query

    select * from ds_leaderboard where country='India';

|   |   |
|---|---|
| Query time | 20 ms |  
| No. of records | 1597 |  
| Index used | used index on country |  

### Query

    select * from ds_leaderboard where country='India';

|   |   |
|---|---|
| Query time | 155 ms |  
| No. of records | 1597 |  
| Index used | forced to ignore index on country |  

