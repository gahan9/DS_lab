-- select * from ds_leaderboard;
-- select * from ds_leaderboard where language_id=1;
-- select * from ds_leaderboard ignore index(pl) where language_id=1;
-- select name,language_id from ds_leaderboard where language_id between 1 and 5;
EXPLAIN SELECT * FROM ds_leaderboard WHERE country='India' GROUP BY language_id
