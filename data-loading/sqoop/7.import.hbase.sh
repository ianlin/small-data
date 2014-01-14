#!/bin/bash

sqoop import --connect "jdbc:mysql://localhost/hadoop" --table user --username cloudera -P --hbase-table table1 --column-family info --hbase-create-table -m 1
