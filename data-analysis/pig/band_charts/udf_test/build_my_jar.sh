#!/bin/bash
java_name='ScoreMap'
package_name='my_pig_java_udfs'
class_path='/usr/lib/pig'
class_jar='pig.jar'
rm -rf "$package_name"
mkdir -p "$package_name"
javac -d "$package_name" -cp "$class_path/$class_jar:`hadoop classpath`" "$java_name.java"
jar -cf "$package_name.jar" "$package_name"
