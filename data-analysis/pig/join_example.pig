row_user_login = load '/home/cloudera/small-data/data-analysis/data/test_user_login' as (uuid:chararray, name:chararray, password:chararray);
row_user_data = load '/home/cloudera/small-data/data-analysis/data/test_user_data' as (uuid:chararray, email:chararray, iq:int, score:int);
--DUMP row_user_login;
--DUMP row_user_data;

after_join = JOIN row_user_login BY uuid RIGHT OUTER, row_user_data BY uuid;
DUMP after_join;
