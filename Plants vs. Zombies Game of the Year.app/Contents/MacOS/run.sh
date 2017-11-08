#!/bin/bash
steamid=3590
log="/tmp/pvz"
rm -f $log
touch $log
path=$(dirname "$0")

find $HOME/Library/Application\ Support/Steam/userdata -path '*/3590/remote/user*.dat' -not -name 'users.dat' -exec python "$path/convert.py" mac {} 1>>$log 2>>$log \;

open -W steam://run/$steamid

find $HOME/Library/Application\ Support/Steam/userdata -path '*/3590/remote/user*.dat' -not -name 'users.dat' -exec python "$path/convert.py" windows {} 1>>$log 2>>$log \;
