Notes on "Bayesian Combination of States Polls and Election Forecasts" by Kari Lock and Andrew Gelman, 2010.

# Section 1: Introduction

Prior data: 2004 election results
Merged with: poll data
Posterior: position of state relative to the national popular vote

National popular vote:
Prior: "Bread-and-peace"
Merged with: poll data

"Not meant to provide the best method for forecasting the national vote but to provide a forecasting method that separates the national vote and the state positions relative to the national vote. This separation allows us to better incorporate historical data on state positions with polling data."

"changes in public opinion […] with wide national swings and fairly stable spatial distributions relative to the national average."

Does it make sense to do it this way? Why not estimate the states, then combine to get the national vote? (Wouldn't get to use Hibbs' prior, for one.)

# Section 2: Past Election Results

How much does a state's voting record in the last election relate to the next election? They look at data from presidential elections 1976–2004. (Why only back to 1976? "State results correlate strongly (.79 <= r <= .95) for adjacent elections after 1972, whereas the correlations between the 1972 and the 1976 elections is only .11").

Looking at the scatterplots for democratic vote in adjacent years, we see proportions tend to be _uniformly_ higher or lower  than the previous year. Authors claim this shows varying nationwide popularity, and that states' "relative partisanship" tends to stay about the same. (Does this make sense? At first glance, yeah, it looks good.)

They say that this is then why they look at _relative state positions_ (rather than estimating states' votes directly?).

They say they tried using data from many past elections, but found that "not much is gained" except for the most recent one. "We imagine that with careful adjustment for economic and political trends, there is useful information from earlier presidential races (as well as data from other elections), but in this paper, we keep things simple[.]"

Center state votes around national votes.

Adjust for home state "We attribute 6% … of the vote for Bush and Kerry in Texas and Massachusetts, respectively, to a home-state advantage, and we add that same amount in the forecast for McCain in Arizona and Clinton in New York or Obama in Illinois."

How much do state positions vary from election to election? Math: Let $d_{s,y}$ be the relative position for state $s$ in year $y$. Then estimate $var(d_{s,2008} | d_{s,2004})$ by $\frac{1/7} \sum_{i=1}^7 (d_{s,y_i+1} - d_{s,y_i})^2$, where $y$ stands for election years 1976—2004. With only seven data points, how reliable are these estimates? They say they could assume a common variance estimate for all states, but instead use _shrinkage estimation_, or _partial pooling_, (what are these? Sounds like they move each estimate towards the overall mean. They say they determine the amount via a hierarchical model, "lmer" in R, based on "comparisons of within-state and between-state variability." Gelman seems to really like hierarchical models?) "Before pooling, the estimates of SD for each state range from 0.012 to 0.073, with complete pooling […] 0.37 and after our partial pooling […] 0.029 to 0.055." (So they reduced variance of their estimates? Does this make sense? Probably math behind pooling supports this.) "From the normal approximation, we can expect the difference in 2008 to fall within 0.06 of the 2004 state difference for the most consistent states and up to 0.11 away for the least consistent states." (Normal approximation? Is that the CLT?)

# Section 3: Pre-election polls

Polls have about 0.02 SD from true population on basis of sampling variability (gotta look at this. Bernoulli / binomial distribution math?). Some people use this and Monte Carlo to generate many "true" population estimates, but authors say, Hey it's only February!

Estimate national-level variance in vote intention before election using Gallup polls in presidential elections 1952–2004. Lots of math, get $\hat{var}(p_t | p_0)$, where $p_t$ is the "true national proportion who intended to vote for the Democratic candidate, $t$ months before the election" and $p_0$ is the "vote share in the actual election." This is an estimate of "uncertainty in the underlying true proportion who would vote Democratic $t$ months before the election." (Does this make sense?)

Graph, fit a linear trend to get variance estimates for each month.

Then do the same for uncertainty in relative position of states at $t$ months before election. Assume common variance for all states, taking a weighted average on poll size. "differences in estimated variances between […] different sorts of states were small and not statistically significant." Also estimate the actual relative position of states at month $t$ using national popular polls.

# Section 4: Posterior distribution

**Looking at relative positions of states:**
Poll model as $\hat{d_{s,t}}|d_{s,0}$: the distribution of a state poll conducted $t$ months before the election.
Prior model as $d_{s,0}|d_{s,2004}$: the distribution of state relative positions in 2008, given its position in 2004
Both are normal distributions, on the basis that polls are pretty large samples and that generally they didn't see outliers in state elections results (they add, whoops, Hawaii in 2008 was an outlier).
Normal-normal mixture model weighted by _information_, "the reciprocal of variance" (what?).
Posterior for true state relative positions at time of election!
They note that, e.g. in February variance in polling data is much larger than variance in the prior, so the posterior will be more heavily weighted towards the prior (TODO: why? Bayesian mixtures).
Note that it didn't work for e.g. Texas which was estimated as a toss-up state.

**National popular vote:**
Prior is the Hibbs prior: growth of per capita income, and U.S. military casualties abroad. Variance estimated by success in prior elections.
Poll is distribution of national poll conducted $t$ months before the election.
Note that weights on mixing to get the posterior automatically change as we get closer to the election!

**Proportion voting Democratic:**
Simulate 100,000 elections, each time: drawing a national popular vote, then drawing a relation position for each state and combining with the popular vote. This gives you the simulated electoral vote outcomes.