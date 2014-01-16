#!/bin/bash

mysql -ucloudera -pcloudera hadoop -e 'create table if not exists big_table (id int(11) not null primary key, name varchar(50), data varchar(50))'

for i in `seq 1 10000`;do
    mysql -ucloudera -pcloudera hadoop -e "insert into big_table values($i, 'str$i', 'data$i')"
done
