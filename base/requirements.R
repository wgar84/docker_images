packs_to_install = c(
	'RPostgreSQL',
	'tidyverse',
	'plyr',
	'dplyr',
	'purrr',
	'devtools',
	'doMC',
	'RColorBrewer',
	'rmarkdown',
	'IRkernel',
	'tm',
	'stringr',
	'stringi',
	'ptstem',
	'stm',
	'wordcloud',
	'qdapRegex'
)

install.packages(packs_to_install, dependencies=TRUE, repos='http://cran.rstudio.com/')
