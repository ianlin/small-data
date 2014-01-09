#!/bin/bash

sqoop import --connect "jdbc:mysql://localhost/hadoop" --username cloudera -P --target-dir user4 --query 'select id, name from user where id <= 3 AND $CONDITIONS' -m 1
