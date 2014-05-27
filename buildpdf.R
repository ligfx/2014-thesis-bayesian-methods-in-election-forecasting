#!/usr/bin/env Rscript

if (!"knitr" %in% installed.packages()) {
  install.packages('knitr', repos='https://cran.r-project.org')
}
if (!"tinytex" %in% installed.packages()) {
  install.packages('tinytex', repos='https://cran.r-project.org')
}
if (!"functional" %in% installed.packages()) {
  install.packages('functional', repos='https://cran.r-project.org')
}
if (!tinytex::is_tinytex()) {
  tinytex::install_tinytex()
}

if (!file.exists("strausswalk.data")) {
  source("strausswalk.R")
}

options(tinytex.verbose=TRUE)
knitr::knit2pdf('thesis.Rnw')
