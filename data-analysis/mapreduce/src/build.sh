#!/bin/bash

javac -cp /usr/lib/hadoop/*:/usr/lib/hadoop/lib/*:/usr/lib/hadoop-mapreduce/*:/usr/lib/hadoop-mapreduce/lib/*:/usr/lib/hadoop-hdfs/*:/usr/lib/hadoop-hdfs/lib/*:/home/cloudera/small-data/data-analysis/lib/* -d jardir BandCharts.java BandChartsMapper.java BandChartsReducer.java

if [[ $? -eq 0 ]]; then
    jar -cvf BandCharts.jar -C jardir/ .
fi
