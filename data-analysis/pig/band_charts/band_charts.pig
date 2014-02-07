orig_records = LOAD 'input/band_charts.csv'
        AS (band:chararray, album:chararray, score:int);

bands_has_winner = FILTER orig_records BY score == 1;

grouped_bands = GROUP bands_has_winner BY band;

best_band = FOREACH grouped_bands GENERATE group, COUNT(bands_has_winner.score) AS times;
--best_band2 = ORDER best_band BY
DUMP best_band;
--STORE good_toilet_group INTO 'output/toilet_ans' USING PigStorage();
