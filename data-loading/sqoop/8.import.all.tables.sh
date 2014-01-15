#!/bin/bash

sqoop import-all-tables --connect "jdbc:mysql://localhost/hadoop" --username cloudera -P
