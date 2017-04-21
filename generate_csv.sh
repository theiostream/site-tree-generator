#!/bin/bash

for snapshot in $1/*.snapshot; do
	filename=$(basename $snapshot)
	pure_snapshot="${filename%.*}"
	echo $pure_snapshot
	python3 ./parser/dir-parser.py $1 ${pure_snapshot} > ./csv/${pure_snapshot}.csv
done
