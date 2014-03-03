#!/usr/bin/env python

import pandas as pd
import pandas.io.sql
import rpy2.robjects
from rpy2.robjects.packages import importr
import sqlite3

base = importr('base')
lme4 = importr('lme4')
stats = importr('stats')
data_frame = rpy2.robjects.r['data.frame']

def ndarray_to_rvector(array):
	if array.dtype == 'O':
		return rpy2.robjects.StrVector(array)
	elif array.dtype == 'float64':
		return rpy2.robjects.FloatVector(array)
	else:
		raise ArgumentError(array.dtype)

def lmer(formula, data):
	for k in data.columns:
		rpy2.robjects.globalenv[k] = ndarray_to_rvector(data[k])
	ret = lme4.lmer(formula)
	for k in data.columns:
		del rpy2.robjects.globalenv[k]
	return ret

db = sqlite3.connect('presidential.sqlite3')

statement = "SELECT y.state, round(y_next.democratrelative - y.democratrelative, 3) AS diff FROM states y JOIN states y_next WHERE y.state == y_next.state AND y.year + 4 == y_next.year + 0;"
states = pd.io.sql.read_frame(statement, db)

states['diff2'] = states['diff'] * states['diff']
print states['diff']
print states['diff2']

states.to_csv('diff.csv')

partial = lmer("diff2 ~ (1|state) - 1", states)
print "Overall" base.summary(partial).rx('coefficients')[0][0]
print stats.coef(partial)