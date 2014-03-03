#!/usr/bin/env bash

database="presidential.sqlite3"

(

	echo "create table summary(year, democrat);"
	echo "create table states(year, state, democrat, democratrelative);"

	for i in $(jot 8 1976 2004); do
		python csv_to_sqlite3.py states$i $i-data.csv
		python csv_to_sqlite3.py summary$i $i-summary.csv
		echo "insert into summary select '$i', round(DemVotesMajorPercentAll/100, 4) from summary$i;"
		echo "insert into states select '$i', Area, round(DemVotesMajorPercent/100, 4), round(DemVotesMajorPercent/100 - summary.democrat, 4) from states$i join summary on summary.year = '$i';"
		echo "drop table summary$i;"
		echo "drop table states$i;"
	done

) | sqlite3 "$database"