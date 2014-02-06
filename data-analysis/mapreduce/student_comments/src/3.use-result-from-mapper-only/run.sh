#!/bin/bash

hadoop jar StudentComments.jar StudentComments -D mapred.child.java.opts=-Xmx1G mapreduce_output/student_comments_mapper_only/part-* mapreduce_output/student_comments_use_result_from_mapper_only
