--orig_records = LOAD 'input/public_toilet' USING PigStorage(',')
orig_records = LOAD '/home/cloudera/small-data/data-analysis/data/public_toilet' USING PigStorage(',')
		AS (id:chararray, name:chararray, total:float, lv1:float, lv2:float, lv3:int, lv4:int, special:int, address:chararray);

address_key = FOREACH orig_records GENERATE
		REGEX_EXTRACT(address, '^\u81fa\u5317\u5e02([^\u5340\u5e02]+\u5340).*', 1) AS area:chararray,
		total, lv1 AS good_cnt, lv3, lv4, ( (lv1 + lv2) / total ) AS good_percent:float, special;

address_key1 = FILTER address_key BY area IS NOT NULL;

grp_key = GROUP address_key1 BY area;

good_toilet_group = FOREACH grp_key {
		address_key2 = FILTER address_key1 BY special == 1 AND good_percent >= 0.75 AND total > 0;
		GENERATE
			group, COUNT(address_key1) AS total , COUNT(address_key2) AS goods,
			SUBSTRING((chararray)((float)COUNT(address_key2)/(float)COUNT(address_key1)),0,4) AS good_rate;
}
DUMP good_toilet_group;
--STORE good_toilet_group INTO './test_ans_relation' USING PigStorage('\t');
