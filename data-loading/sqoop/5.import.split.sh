#!/bin/bash

sqoop import --connect "jdbc:mysql://localhost/hadoop" --table big_table --username cloudera -P --split-by name --target-dir big_table_1
