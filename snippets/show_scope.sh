#!/bin/bash
# Get the scope of given class in a given file
# Then show the evelution of the class via git log -L
# usage: show_scope [classname] [filename]
# cname='class HttpAuthHandler'
# fname='HttpAuthHandler.java'
 
cname=$1
fname=$2
begin=$(grep -n ".*$cname.*" $fname | grep -Eo "^[0-9]{1,5}")
num_lines=$(grep -zPo ".*$cname.*(\{([^{}]++|(?1))*\})" $fname | wc -l)
end=$((begin + num_lines - 1))
git log -L $begin,$end:$fname 
