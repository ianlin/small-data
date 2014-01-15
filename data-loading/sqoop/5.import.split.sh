#!/bin/bash

time sqoop import --connect "jdbc:mysql://localhost/hadoop" --username cloudera -P --target-dir user6 --query 'select id, name from user where id <= 3 AND $CONDITIONS' --split-by name -m 2
