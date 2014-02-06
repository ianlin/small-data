select band, count(*) as cnt from band_charts where rank=1 group by band order by cnt desc;
