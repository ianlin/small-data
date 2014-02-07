--LOAD ORIGINAL DATA
CREATE TABLE toilet_orig (id INT, name STRING, total INT, lv1 INT, lv2 INT, lv3 INT, lv4 INT, special INT, address STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',';


LOAD DATA INPATH 'input/public_toilet'
OVERWRITE INTO TABLE toilet_orig;


CREATE TABLE toilet_address_key (area STRING, total INT, good_cnt INT, good_percent FLOAT, special TINYINT);

--Henry: In Hive, can use Chinese directly.
INSERT OVERWRITE TABLE toilet_address_key
SELECT regexp_extract(address, '^臺北市([^市區]+區).*', 1), total, lv1, (( CAST(lv1 AS FLOAT) + CAST(lv2 AS FLOAT)) / CAST(total AS FLOAT)), special FROM toilet_orig;

--SELECT regexp_extract(address, '^\u81fa\u5317\u5e02([^\u5340\u5e02]+\u5340).*', 1), total, lv1, (( CAST(lv1 AS FLOAT) + CAST(lv2 AS FLOAT)) / CAST(total AS FLOAT)), special FROM toilet_orig;



CREATE TABLE toilet_address_count (area STRING, total_point INT);
INSERT OVERWRITE TABLE toilet_address_count
SELECT area, count(*) FROM toilet_address_key GROUP BY area;



CREATE TABLE best_toilet (area STRING, total_point INT, good_point INT, good_percent FLOAT);
INSERT OVERWRITE TABLE best_toilet
SELECT area, 0, COUNT(area), 0.00
FROM toilet_address_key
WHERE special = 1 AND good_percent >= 0.75 AND total > 0 AND area IS NOT NULL AND area != '' GROUP BY area;



SELECT best_toilet.area, toilet_address_count.total_point, best_toilet.good_point, ( CAST( best_toilet.good_point AS FLOAT) / CAST( toilet_address_count.total_point AS FLOAT) ) AS good_percent
FROM best_toilet LEFT OUTER JOIN toilet_address_count ON ( best_toilet.area=toilet_address_count.area) WHERE toilet_address_count.area IS NOT NULL AND toilet_address_count.area != '';
