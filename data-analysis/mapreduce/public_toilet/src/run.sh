#!/bin/bash

hadoop jar PublicToilet.jar PublicToilet -D mapred.reduce.tasks=0 input/public_toilet mapreduce_output/public_toilet
