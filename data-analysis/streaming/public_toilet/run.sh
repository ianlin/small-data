#!/bin/bash

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.4.0.jar -input input/public_toilet -output streaming_output/public_toilet -mapper mapper.py -file mapper.py -reducer reducer.py -file reducer.py
