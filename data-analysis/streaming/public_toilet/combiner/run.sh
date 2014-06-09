#!/bin/bash

hadoop jar /usr/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming.jar -input input/public_toilet -output streaming_output/public_toilet -mapper mapper.py -file mapper.py -reducer reducer.py -file reducer.py -combiner combiner.py -file combiner.py
