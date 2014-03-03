#!/usr/bin/env python

from itertools import *
import re
import requests

years = range(1976, 2008, 4)

def splitter(lines):
	return "\n".join(takewhile(lambda _: _.strip() != ",", lines))

for y in years:
	print y
	url_template = "http://library.cqpress.com/elections/download-data-results.php?filetype=1&office=1&areatype=1&year={year}&format=3&license=on"
	url = url_template.format(year=y)
	resp = requests.get(url).text.strip()
	lines = iter(re.split("\r?\n", resp))

	title = splitter(lines)
	data = splitter(lines)
	summary = splitter(lines)

	with open("{year}-title.txt".format(year=y), "w") as f:
		f.write(title)

	with open("{year}-data.csv".format(year=y), "w") as f:
		f.write(data)

	with open("{year}-summary.csv".format(year=y), "w") as f:
		f.write(summary)