#!/bin/bash

function install_packages() {
    # install lxml python module
    pkgs="python-lxml"
    sudo yum install -y $pkgs
}

function setup_mysql() {
    # install mysql server
    sudo yum install -y mysql mysql-server

    # start mysql server daemon
    sudo chkconfig --level 2345 mysqld on
    sudo service mysqld start

    # change root password
    /usr/bin/mysqladmin -u root password 'root' # for demo purpose, do not set this sort of password in a real world. :)

    # delete all user who are not root
    mysql -uroot -proot -e "DELETE FROM mysql.user WHERE NOT (host='localhost' and user='root');"
    mysql -uroot -proot -e "FLUSH PRIVILEGES;"

    # remove anonymous access to the database(s)
    mysql -uroot -proot -e "DELETE FROM mysql.user WHERE User = '';"
    mysql -uroot -proot -e "FLUSH PRIVILEGES;"

    # add a new database 'hadoop'
    mysql -uroot -proot -e "CREATE DATABASE hadoop;"
    mysql -uroot -proot -e "FLUSH PRIVILEGES;"
    echo "Database 'hadoop' has been created."
    
    # add a new user 'cloudera'
    mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON *.* TO 'cloudera'@'localhost' IDENTIFIED BY 'cloudera' WITH GRANT OPTION;"
    mysql -uroot -proot -e "FLUSH PRIVILEGES;"
    echo "User 'cloudera' has been created."
    
    # add a new user with database admin privileges for database 'hadooptest'
    mysql -uroot -proot -e "GRANT ALL PRIVILEGES ON hadooptest.* TO 'cloudera'@'localhost' IDENTIFIED BY 'cloudera';"
    mysql -uroot -proot -e "FLUSH PRIVILEGES;"

    # create table 'user'
    mysql -ucloudera -pcloudera hadoop -e "CREATE TABLE user (id int primary key, name varchar(50), mobile varchar(50), location varchar(50));"
    echo "Table 'user' has been created in database 'hadoop'."

    # insert data to table 'user'
    mysql -ucloudera -pcloudera hadoop -e "INSERT INTO user VALUES (1, 'Ian', '1111', 'Taipei');"
    mysql -ucloudera -pcloudera hadoop -e "INSERT INTO user VALUES (2, 'Henry', '2222', 'Taichung');"
    mysql -ucloudera -pcloudera hadoop -e "INSERT INTO user VALUES (3, 'Peter', '3333', 'Tainan');"
    mysql -ucloudera -pcloudera hadoop -e "INSERT INTO user VALUES (4, 'John', '4444', 'Hualien');"
    mysql -ucloudera -pcloudera hadoop -e "INSERT INTO user VALUES (5, 'Harry', '5555', 'New Taipei');"
    echo "User data has been inserted to table 'user' in database 'hadoop'."
}

function main() {
    install_packages
    setup_mysql
}

main
