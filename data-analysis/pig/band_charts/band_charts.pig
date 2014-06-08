orig_records = LOAD '/home/cloudera/small-data/data-analysis/data/band_charts.csv'
--orig_records = LOAD 'input_data/band_charts.csv'
        AS (band:chararray, album:chararray, score:int);

bands_has_winner = FILTER orig_records BY score == 1;

grouped_bands = GROUP bands_has_winner BY band;

best_band = FOREACH grouped_bands GENERATE group, COUNT(bands_has_winner.score) AS times;
best_band2 = ORDER best_band BY times DESC;
DUMP best_band2;
--EXPLAIN best_band2;
--STORE best_band2 INTO 'output/best_band_ans' USING PigStorage(',');
