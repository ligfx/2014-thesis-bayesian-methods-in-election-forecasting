import numpy as np
import pandas as pd

srrs2 = pd.read_csv("srrs2.dat")
srrs2.columns = (c.strip() for c in srrs2.columns)

srrs2 = srrs2[srrs2['state'] == 'MN']

cty = pd.read_csv("cty.dat")
cty = cty[cty['st'] == 'MN']

def normalize_county(cty):
	return cty.lower().replace(" ", "")

cty['cty'] = cty['cty'].map(normalize_county)
srrs2['county'] = srrs2['county'].map(normalize_county)

# Dropping the 41 items that can't decide whether they're in a basement or not
srrs2 = srrs2[(srrs2['floor'] == 0) | (srrs2['floor'] == 1)]
srrs2 = srrs2[srrs2['activity'] > 0]
srrs2['basement'] = srrs2['floor'] == 0

srrs2['uranium_in_county'] = srrs2['county'].map(lambda c: list(cty[cty['cty'] == c]['Uppm'])[0])

# Okay, we want a matrix Z with n rows and 170 columns, where the first column
# is an indicator on county 1, the second column is an indicator on county 1
# multiplied by the uranium level in county 1, the third column is an
# indicator on county 2, and so on.

counties = srrs2['county'].unique()

from itertools import chain
z = []
for (i, row) in srrs2.iterrows():
	zrow = list(chain.from_iterable(
		(1 if row['county'] == c else 0,
		row['uranium_in_county'] if row['county'] == c else 0)
		for c in counties))
	z.append(zrow)

z = np.matrix(z)
assert z.shape == (len(srrs2), 170)

# Okay, we also want a matrix X with n rows and two columns, where the first
# column is 1 and the second column is an indicator on basement
x = []
for (i, row) in srrs2.iterrows():
	xrow = [1, 1 if row['basement'] else 0]
	x.append(xrow)

x = np.matrix(x)
assert x.shape == (len(srrs2), 2)

# We also want Y, where Y is an n-length column vector of logradon
y = np.matrix(np.log(srrs2['activity'])).T
assert y.shape == (len(srrs2), 1)

