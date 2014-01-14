#!/bin/bash

sqoop import --connect "jdbc:mysql://localhost/hadoop" --table user --where "id <= 3" --username cloudera -P --target-dir user3 -m 1
