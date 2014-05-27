#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

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

srrs2['uranium_in_county'] = srrs2['county'].map(lambda c: list(cty[cty['cty'] == c]['Uppm'])[0])

srrs2['jitter'] = np.random.normal(0, 0.01, len(srrs2))
lacquiparle = srrs2[srrs2['county'] == 'lacquiparle']
lacquiparle_uranium = list(lacquiparle['uranium_in_county'])[0]

# Model is like: y_i = gamma_0 + gamma_1 * u * G + beta * x_i
# log(radon) = g0 + g1 * log(uranium_in_county) + g2 * in_basement

pooled = smf.ols('np.log(activity) ~ floor', data=srrs2).fit()
print pooled.summary()
unpooled = smf.ols('np.log(activity) ~ floor + county - 1', data=srrs2).fit()
print unpooled.summary()

# Values from lmer(logradon ~ floor + (1 | county), srrs2) in R
def partial_predict_lacquiparle(floor):
	return 1.9169895 + -0.640674 * floor

plt.figure()
plt.grid()
plt.scatter(srrs2['floor'] + srrs2['jitter'], np.log(srrs2['activity']))
plt.plot([-0.1, 1.1], [pooled.predict({'floor': -0.1}), pooled.predict({'floor': 1.1})], 'b--')
plt.xlim([-0.1, 1.1])
plt.ylim([-1.5, 3.5])

plt.figure()
plt.grid()
plt.scatter(lacquiparle['floor'] + lacquiparle['jitter'], np.log(lacquiparle['activity']))
plt.plot([-0.1, 1.1], [pooled.predict({'floor': -0.1}), pooled.predict({'floor': 1.1})], 'b--')
plt.plot([-0.1, 1.1], [
	unpooled.predict({'county': ['lacquiparle'], 'floor': -0.1}),
	unpooled.predict({'county': ['lacquiparle'], 'floor': 1.1})], 'r')
plt.plot([-0.1, 1.1], [partial_predict_lacquiparle(-0.1), partial_predict_lacquiparle(1.1)], 'k')
plt.xlim([-0.1, 1.1])
plt.ylim([-1.5, 3.5])