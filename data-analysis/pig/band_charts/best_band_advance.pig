--Register 'pig_python_util.py' using jython as myfuncs;
Register 'pig_python_util.py' using org.apache.pig.scripting.jython.JythonScriptEngine as myfuncs;
--Register '/home/cloudera/small-data/data-analysis/pig/band_charts/udf_test/my_pig_java_udfs.jar';
REGISTER /usr/lib/pig/piggybank.jar;

--orig_records = LOAD 'input/band_charts.csv'
orig_records = LOAD '/home/cloudera/small-data/data-analysis/data/band_charts.csv'
		AS (band:chararray, album:chararray, score:int);

--Using Python UDF
bands_has_winner = FOREACH orig_records GENERATE band, myfuncs.ScoreMap(score);

grouped_bands = GROUP bands_has_winner BY band;


--best_band = FOREACH grouped_bands GENERATE group, SUM(bands_has_winner.score) AS total_score;
--Using PiggyBank Example
best_band = FOREACH grouped_bands GENERATE org.apache.pig.piggybank.evaluation.string.UPPER(group), SUM(bands_has_winner.score) AS total_score;
best_band2 = ORDER best_band BY total_score DESC;
DUMP best_band2;
