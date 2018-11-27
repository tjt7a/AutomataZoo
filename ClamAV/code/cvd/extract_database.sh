#!/bin/bash
if [ $# -ne 1 ]
then
    echo "USAGE: ./extract_database.sh <cvd_file.cvd>"
    exit 1
fi

sigtool --unpack ${1}

mv *.ndb ../databases

echo "Unpacked .nbd databases to ../databases directory..."
