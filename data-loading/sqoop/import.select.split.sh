#!/bin/bash

sqoop import --connect "jdbc:mysql://localhost/hadoop" --username cloudera -P --target-dir user5 --query 'select id, name from user where id <= 3 AND $CONDITIONS' --split-by id -m 2
