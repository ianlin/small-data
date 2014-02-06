create table public_toilet (id INT, name STRING, amount INT, score_first INT,
                            score_second INT, score_third INT, score_fourth INT,
                            handicapped INT, address STRING, longitude FLOAT, latitude FLOAT)
row format delimited
fields terminated by ',';
