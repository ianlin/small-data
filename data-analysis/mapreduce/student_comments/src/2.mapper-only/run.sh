#!/bin/bash

hadoop jar StudentComments.jar StudentComments -D mapred.reduce.tasks=0 -D mapred.child.java.opts=-Xmx1G input/student_comments mapreduce_output/student_comments_mapper_only
