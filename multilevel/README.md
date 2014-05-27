# Bibliography

* [Gelman, 2005. Multilevel (Hierarchical) Modeling: What It Can and Cannot Do](http://www.stat.columbia.edu/~gelman/research/published/multi2.pdf): main paper.
* [Price, Nero, and Gelman, 1996. Bayesian Prediction of Mean Indoor Radon Concentrations for Minnesota Counties](http://www.stat.columbia.edu/~gelman/research/published/price.pdf): description of data.
* [Gelman, Stevens, and Chan, 2003. Regression Modeling and Meta-Analysis for Decision Making: A Cost-Beneﬁt Analysis of Incentives in Telephone Surveys](http://www.stat.columbia.edu/~gelman/research/published/jbes01m045r3.pdf): Gelman (2005) says, "We fit the model using hierarchical Bayes methods."
* [Nero et al., 1994. Statistically Based Methodologies for Mapping of Radon 'Actual' Concentrations: The Case of Minnesota](http://rpd.oxfordjournals.org/content/56/1-4/215.short): Meh. No mention of what NURE data they used.
* [Snijders, 2012. Multilevel Analysis (Slides)](http://www.stats.ox.ac.uk/~snijders/MLB_new_S.pdf): slides on multilevel regressions.
* [NYC Predictive Analytics, 2010. An Introduction to Multilevel Regression Modeling for Prediction (Slides)](http://slideshare.net/NYCPredictiveAnalytics/an-introduction-to-multilevel-regression-modeling-for-prediction)
* http://www.math.montana.edu/~jimrc/classes/stat506/notes/chapter12-nup.pdf: Good slides, good graphs.
* [Chapter 12: Multilevel linear models: the basics](http://www.uky.edu/AS/PoliSci/Peffley/pdf/chapter12%20R.pdf): YES! Describes how to use lmer to fit partially-pooled regression models in R.

# To Read

* [A Novice's Guide to Understanding Mixed Effects Models](http://www2.hawaii.edu/~kdrager/MixedEffectsModels.pdf)
* [The Basic Two-Level Regression Model](http://joophox.net/mlbook2/Chapter2.pdf)

# Data

* [The HIGH-RADON PROJECT: Files and Documentation](http://energy.lbl.gov/ie/high-radon/files.html)
* [National Uranium Resource Evaluation (NURE) Hydrogeochemical and Stream Sediment Reconnaissance data](http://mrdata.usgs.gov/metadata/nurehssr.faq.html): http://mrdata.usgs.gov/nure/sediment/select.php?place=fUS27&div=fips
* [Gelman and Hill. Data Analysis Using Regression and Multilevel/Hierarchical Models](http://www.stat.columbia.edu/~gelman/arm/): data on county uranium levels in radon/cty.dat

## srrs2.dat

SRRS data for year 2 (87-88). ASCII SRRS data (screening measurements) for AZ, IN, MA, Reg 5 Indian lands, MN, MO, ND, and PA.

*Two state variables*: ' state' contains 'R5' values, which stands for Region 5 Indian lands. ' state2' reports measurements in Region 5 Indian lands as measurements from the state they are geographically located inside. Gelman (2005) uses the 919 values where ' state' is 'MN'.

*Counties*: Gelman (2005) uses 85 counties of Minnesota. A quick check shows I also have 85 counties in Minnesota. Good!

## cty.dat

Has two extra counties than SRRS2, GRANT and REDLAKE. Also has two measurements for CARVER and LACQUIPARLE, at slightly different longitudes and latitudes, but the Uppm measurements are the same. 

# Gelman (2005) model

y_ij = a_j + beta * x_ij + sigma_y^2
a_j = gamma_0 + gamma_1 * u_j + sigma_a^2
where y_ij is the log radom measurement in house i in county j, x_ij is whether that measurement was taken in the basement, and u_j is the log uranium level in county j.

Note we could also write this as 

y_ij = gamma_0 + gamma_1 * u_j + beta * x_ij + sigma_a^2 + sigma_y^2
=> y_i = gamma_0 + gamma_1 * u * G + beta * x_i + sigma_a^2 * GG^t + sigma_y^2

where G is the matrix of county indicators, and GG^t means what??

Then if we wanted to predict a house in county j, the risk would be

gamma_0 + gamma_1 * u_j + beta * (basement?) + error

Thus we share general risk and effect of uranium in soil, but each county gets a different slope between basement/not in basement.

What? This isn't what it looks like in the graphs. Graphs look like: slope is the same among each county (for complete-, no-, and partial-pooling). Complete-pooling obviously should have the same slope, and has the same intercept as well (this is ignoring county differences). No pooling looks like it has the same slope, but sometimes wildly different intercepts (e.g. in Lac Qui Parle, which has two measurements). Partial-pooling looks like it has the same slope, but still different intercepts, though closer to the complete-pooling intercepts.

Right! This is exactly what we did! Interpreting gamma_0 + gamma_1 * u_j as the intercept in the graphs. So each county has a different intercept because it has a different uranium soil content, but they all get the same slope.

WAIT. Shouldn't complete pooling also give different intercepts? Because we have some estimate for the coefficient on uranium levels in the soil?

Why is this interesting? Their graphs and cross-validation show that partial-pooling tends to do better than either complete-pooling or no-pooling. Partial-pooling allows between-county


# Gelman, Stevens, and Chan (2003) model

Re-doing the data analysis of a previous meta-analysis by Singer et al. (1999), which looked at 39 surveys, which among them had 101 experimental conditions.

Starts describing some complicated algorithm?

# Multilevel Analysis: Techniques and Applications Chapter 2

* Classes j = 1..J
* # of Pupils n_j
* Popularity Y (0 .. 10)
* Pupil gender x_1 (0 = boy, 1 = girl)
* Pupil extraversion x_2 (1 .. 10)
* Class teacher experience z (2 .. 25)
2000 pupils in 100 classes

We can set up separate regression equations for each class to predict popularity as follows:

popularity_ij = beta_0j + beta_1j * gender_ij + beta_2j * extraversion_ij + e_ij

Assume each class has a different intercept beta_0j and different slope coefficients beta_1j and beta_2j. Next, explain the regression coefficients at the class level:

beta_0j = gamma_00 + gamma_01 * teacherexperience_j + u_0j
beta_1j = gamma_10 + gamma_11 * teacherexperience_j + u_1j
beta_2j = gamma_20 + gamma_21 * teacherexperience_j + u_2j

This also is equivalent to:

popularity_ij = gamma_00 + gamma_01 * teacherexperience_j + u_0j + gamma_10 * gender_ij + gamma_11 * teacherexperience_j * gender_ij + u_1j * gender_ij + gamma_20 * extraversion_ij + gamma_21 * teacherexperience_j * extraversion_ij + u_2j * extraversion_ij

or

Popularity ~ 1 + Gender + Extraversion + TeacherExperience + Gender*TeacherExperience + Extraversion*TeacherExperience + Error

# old notes

# How do mixed level models work??

Okay: Meng and van Dyk (2008) propose an EM-type algorithm for mixed-effects, based on the `working parameter' method of Meng and van Dyk (1997). Apparently Dempster et al. (1977) in the original EM paper showed how to do mixed-effects. Would the LME4 guy argue that these methods don't talk about how to avoid the singularity problem? Other people have also looked at mixed-effects. After EM comes ECME (Liu and Rubin, 1994). There's also Dynamic ECME (He and Liu, ???). See Varadhan and Roland (2008) for a review of methods for accelerating EM.

- http://cran.r-project.org/web/packages/nlme/nlme.pdf

- http://dx.doi.org/10.1111/1467-9868.00140 Fast EM-type implementations for mixed effects models
- http://lme4.r-forge.r-project.org/lMMwR/lrgprt.pdf: Chapter 5, pg 113. Describes something about iterative things and finding the normalized conditional distribution (!)
- http://www.stat.purdue.edu/~chuanhai/teaching/Stat598A/PinheiroLiuWu.pdf
- http://onlinelibrary.wiley.com/doi/10.1002/1521-4036(200111)43:7%3C881::AID-BIMJ881%3E3.0.CO;2-S/abstract
- http://www.ats.ucla.edu/stat/examples/msm_goldstein/goldstein.pdf: see citation of Bryk and Raudenbush (1992)
- http://sci2s.ugr.es/keel/pdf/specific/articulo/schafer_yucel02.pdf
- http://www.stat.wisc.edu/~bates/reports/MixedComp.pdf
- http://andrewgelman.com/2012/04/17/hierarchicalmultilevel-modeling-with-big-data/
- http://www.stat.columbia.edu/~gelman/research/published/multiple2f.pdf

