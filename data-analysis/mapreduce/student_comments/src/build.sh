#!/bin/bash

javac -cp /usr/lib/hadoop/*:/usr/lib/hadoop/lib/*:/usr/lib/hadoop-mapreduce/*:/usr/lib/hadoop-mapreduce/lib/*:/usr/lib/hadoop-hdfs/*:/usr/lib/hadoop-hdfs/lib/*:/home/cloudera/small-data/data-analysis/lib/* -d jardir StudentComments.java

if [[ $? -eq 0 ]]; then
    jar -cvf StudentComments.jar -C jardir/ .
fi