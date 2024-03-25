#!/usr/bin/env bash

touch data.csv
cp data.csv data.csv.bak
cat <(sed 's/.$//' training.txt) data.csv.bak | sort -u > data.csv
