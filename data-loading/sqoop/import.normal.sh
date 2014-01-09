#!/bin/bash

sqoop import --connect "jdbc:mysql://localhost/hadoop" --table user --username cloudera -P
