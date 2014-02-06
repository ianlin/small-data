#!/bin/bash

hadoop jar StudentComments.jar StudentComments -D mapred.child.java.opts=-Xmx1G input/student_comments mapreduce_output/student_comments_combiner
