#!/bin/bash

sqoop import --connect "jdbc:mysql://localhost/hadoop" --table user --username cloudera -P --hive-import -m 1 --target-dir test --hive-table table1
