#!/usr/bin/env bash

sort -u training.txt | sed 's/.$//' | shuf > data.csv