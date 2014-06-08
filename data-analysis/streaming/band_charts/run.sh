#!/bin/bash

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar -input input/band_charts -output streaming_output/band_charts -mapper mapper.py -file mapper.py -reducer reducer.py -file reducer.py
