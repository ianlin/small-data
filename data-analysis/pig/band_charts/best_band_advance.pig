--Register 'pig_python_util.py' using jython as myfuncs;
Register 'pig_python_util.py' using org.apache.pig.scripting.jython.JythonScriptEngine as myfuncs;

orig_records = LOAD 'input/band_charts.csv'
        AS (band:chararray, album:chararray, score:int);

bands_has_winner = FOREACH orig_records GENERATE band, myfuncs.score_map(score);

grouped_bands = GROUP bands_has_winner BY band;

best_band = FOREACH grouped_bands GENERATE group, SUM(bands_has_winner.score) AS total_score;
best_band2 = ORDER best_band BY total_score DESC;
DUMP best_band2;
