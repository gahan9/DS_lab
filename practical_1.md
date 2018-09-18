[Practical 1](https://github.com/gahan9/DS_lab/blob/master/practical_1.md)
=========== 
> a) Import Database, understand Query execution plan using SQL Yog    
b) Analyze impact of index , type of index on query performance   
  
a) Database Structure 
--------------------- 
- **Database**: *MySQL* 
- **Total data rows in table ds_leaderboard**: *4,00,000* 
- PC Configuration      
    *: Intel® Core™ i3-4130 CPU @ 3.40GHz × 4      
    : ~ 4 GB RAM*    
    
*Table*: **ds_leaderboard**    
    
```sql
CREATE TABLE `ds_leaderboard` (     
    `id` Int( 11 ) AUTO_INCREMENT NOT NULL,    
    `name` VarChar( 64 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,   
    `email` VarChar( 254 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,   
    `organizer` VarChar( 256 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,   
    `score` Double( 22, 0 ) NOT NULL,   
    `time` VarChar( 16 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,   
    `country` VarChar( 128 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,   
    `language_id` Int( 11 ) NULL, PRIMARY KEY ( `id` )   
)  
CHARACTER SET = utf8    
COLLATE = utf8_general_ci    
ENGINE = InnoDB    
AUTO_INCREMENT = 400001;  
```
---  
*Table*:**ds_programminglanguage**    
```sql  
CREATE TABLE `ds_programminglanguage` (  
    `id` Int( 11 ) AUTO_INCREMENT NOT NULL,    
    `name` VarChar( 32 ) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,   
    `version` VarChar( 16 ) CHARACTER SET utf8 COLLATE utf8_general_ci NULL,   
    `release` Date NULL, PRIMARY KEY ( `id` )   
)   
CHARACTER SET = utf8   
COLLATE = utf8_general_ci   
ENGINE = InnoDB   
AUTO_INCREMENT = 13;  
```  
---  
 
 
b) Impact of index 
------------------------
### Case 1  
```sql  
select * from ds_leaderboard;  
```  
| Query time | 1.947 s      
|---:|:---  
| Index used | No index to be used because we are loading all data of all attribute(column)    
> ![](https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/select_all.png)

### Case 2.1 : with index    
```sql  
select * from ds_leaderboard where language_id=1;  
```    
| Query time | 234 ms      
|---:|:---  
| No. of records | 33243
| Index used | index on attribute language_id
> ![](https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/select_all_language_1.png)

### Case 2.2 : without index  (forced to not to use)  
```sql  
select * from ds_leaderboard ignore index(pl) where language_id=1;
```  
| Query time | 291 ms  
|---:|:---|  
| No. of records | 33243      
| Index used | (No index) ignoring index on attribute language_id (index referred as `pl`)
>  ![](https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/select_all_language_without_pl.png)
  
### Case 3.1 : with no index 
```sql    
select name,language_id from ds_leaderboard where language_id between 1 and 5;  
```    
| Query time | 215 ms      
|---:|:---  
| No. of records | 166490      
| Index used | (No index used) (possible key on language_id)      

> ![](https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/select_name.lang_where_lang_range_215ms.png)

    
### Case 3.2 : with index on language_id (force to use)
```sql  
select name,language_id from ds_leaderboard use index(pl) where language_id between 1 and 5;
```  
| Query time | 206 ms
|---:|:---
| No. of records | 166490
| Index used | forced to use index on language_id (pl)
![]()    
    
### Case 4.1 : using index on country 
```sql    
select * from ds_leaderboard where country='India';    
```   
| Query time | 20 ms
|---:|:---  
| No. of records | 1597
| Index used | used index on country
![]()

### Case 4.2 : without index (forced to ignore)
```sql
select * from ds_leaderboard ignore index(ctry) where country='India';    
```
| Query time | 155 ms   
|---:|:---  
| No. of records | 1597  
| Index used | forced to ignore index on country  
>![]()
    
### Case 5.1 : using index on language_id and country
```sql    
select * from ds_leaderboard where country='India' and language_id=1;    
```  
| Query time | 11 ms  
|---:|:---  
| No. of records | 143  
| Index used | Using intersect(pl,ctry); index of language_id and country  
>![](https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/case5_2_index.png)    
    
### Case 5.2 : force to ignore index on country
```sql  
select * from ds_leaderboard ignore index(ctry) where country='India' and language_id=1;    
```  
| Query time | 42 ms  
|---:|:---  
| No. of records | 143  
| Index used | Using index on language_id  
>![]()

### Case 5.3 : force to ignore index on language_id
```sql  
select * from ds_leaderboard ignore index(pl) where country='India' and language_id=1;
```
| Query time | 4 ms  
|---:|:---
| No. of records | 143  
| Index used | Using index on country  
>![](https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/case5_index_on_country.png)
    
### Case 5.4 without index 
```sql
select * from ds_leaderboard ignore index(pl,ctry) where country='India' and language_id=1;
```  
| Query time | 148 ms  
|---:|:---  
| No. of records | 143  
| Index used | No index used; Forced to ignore index |
>![](https://raw.githubusercontent.com/gahan9/DS_lab/master/practical_1/case5_no_index.png)

Summary
------------
In records of `4,00,000` entries `33,243` entries having *language_id* equals to `1` (*As in Case 2*) and just `1597` entries having *country* equals to `India` (*As in Case 4*)and only `143` entries having both (*As in Case 5*).   

In `case 5.1 ` query engine choose to use index of both attribute language_id (pl) and country (ctry) and intersection of it is displayed which took about `11 ms` whereas when we forced to use only index on *country* the result took only `4 ms` but for only using index on *language_id*  it costs `148 ms` 
