#!/usr/bin/env python

import csv
import sys

tablename = sys.argv[1]
csvfilename = sys.argv[2]

with open(csvfilename) as csvfile:
	reader = csv.reader(csvfile)
	header = next(reader)
	print("create table {table}({header});".format(table=tablename, header=",".join(header)))
	print(".mode csv")
	print(".separator ,")
	print(".import {csv} {table}".format(csv=csvfilename, table=tablename))
	print("delete from {table} where ({column}='{column}');".format(table=tablename, column=header[0]))
