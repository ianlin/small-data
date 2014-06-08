a = load '/home/cloudera/small-data/data-analysis/data/pig_test_flatten_example' as (f1:chararray,B: bag {T: tuple(t1:chararray, t2:int, t3:float)});
DUMP a;
/*
b = foreach a {
	sorted = ORDER B by t3 DESC;
	GENERATE f1, sorted;
}
*/
b = foreach a GENERATE f1, FLATTEN(B) as (t1:chararray,t2:int,t3:float);
--a = load '/home/cloudera/small-data/data-analysis/data/pig_test_flatten_example';
--b = foreach a GENERATE FLATTEN($1);
DUMP b;
