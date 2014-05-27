require('lme4')
srrs2 <- read.csv('srrs2.dat')
srrs2 <- subset(srrs2, state == 'MN')
srrs2$logradon <- log(srrs2$activity)

cty <- read.csv('cty.dat')
cty = cty[cty['st'] == 'MN',]

normalize_county <- function(x) tolower(gsub(" ","", x))

srrs2$county <- sapply(srrs2$county, normalize_county)
cty$cty <- sapply(cty$cty, normalize_county)

srrs2 <- subset(srrs2, floor == 0 | floor == 1)
srrs2 <- subset(srrs2, activity > 0)
srrs2$basement = srrs2$floor == 0

srrs2['uranium_in_county'] = srrs2['county'].map(lambda c: list(cty[cty['cty'] == c]['Uppm'])[0])

# pooled <- lm(logradon ~ floor, srrs2)
# summary(pooled)
# unpooled <- lm(logradon ~ floor + factor(county) - 1, srrs2)
# summary(unpooled)

partial <- lmer(logradon ~ floor + (1 | county), srrs2)
coef(partial)