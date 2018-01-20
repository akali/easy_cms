# easy_cms  
Easily install, configure, control [cms](http://cms-dev.github.io/)(Contest Management System v1.3rc0) on remote machines.  

## Preparation  
Change **ip_addresses**, **commands.py**, **constants.py**, **passwords.py** in **config** folder if it needed.  

## Installation of cms  
Start script with **-i** flag and specify indexes of ip addreses numbered from zero.  
Example: **python3 ./easy_cms 0 1 2 3 -i**  

## Updating configs
Start script with **-u** flag and specify indexes of ip addreses numbered from zero.  
Example: **python3 ./easy_cms 0 1 2 3 -u**  

## Starting contest
Start script with **-s** flag and specify indexes of ip addreses numbered from zero.  
Example: **python3 ./easy_cms 0 1 2 3 -s**  

## Stop cms
Start script with **--stop** flag and specify indexes of ip addreses numbered from zero.  
Example: **python3 ./easy_cms 0 1 2 3 -stop**  

## Start AdminWebServer
Start script with **--start_admin** flag and specify indexes of ip addreses numbered from zero.  
Example: **python3 ./easy_cms 0 --start_admin**  

## ...  
You can combine commands.  
Example: **python3 ./easy_cms 0 1 2 3 -i --start_admin**  

You can use **-n** flag to skip generating config files.  
Example: **python3 ./easy_cms 0 1 2 3 -n -u**  

If you combine commands operations executed in this order:  
**Installation**  
**Updating configs**  
**Starting AdminWebServer**  
**Stopping cms**  
**Starting cms**  
