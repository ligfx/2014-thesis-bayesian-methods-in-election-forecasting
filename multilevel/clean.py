import numpy.linalg as la
import sqlite3
import pandas as pd
from pandas.io import sql

def normalize_county(cty):
    return cty.lower().replace(" ", "")

srrs2 = pd.read_csv("srrs2.dat")
srrs2.columns = (c.strip() for c in srrs2.columns)
# Dropping the 41 items that can't decide whether they're in a basement or not
srrs2 = srrs2[(srrs2['floor'] == 0) | (srrs2['floor'] == 1)]
srrs2 = srrs2[srrs2['activity'] > 0]
srrs2['county'] = srrs2['county'].map(normalize_county)

cty = pd.read_csv("cty.dat")
cty['cty'] = cty['cty'].map(normalize_county)

c = sqlite3.connect("cleaned.sqlite3")
sql.write_frame(srrs2, "srrs2", c)
sql.write_frame(cty, "cty", c)

