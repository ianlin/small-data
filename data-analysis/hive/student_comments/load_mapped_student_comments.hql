--CREATE TABLE kv_orig (key STRING, value STRUCT<student:STRING, age:TINYINT, area:STRING, score:TINYINT>)
--ROW FORMAT DELIMITED
--FIELDS TERMINATED BY '\t' COLLECTION ITEMS TERMINATED BY ',';


--LOAD DATA LOCAL INPATH '/home/cloudera/henry/testdata/student_comments/part-m-00007'
--OVERWRITE INTO TABLE kv_orig;
