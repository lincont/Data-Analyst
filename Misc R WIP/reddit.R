reddit <- read.csv('reddit.csv')

table(reddit$employment.status)
summary(reddit)

str(reddit)

levels(reddit$age.range)

library(ggplot2)
qplot(data = reddit, x = age.range)
reddit <- read.csv('reddit.csv')

table(reddit$employment.status)
summary(reddit)

str(reddit)

levels(reddit$age.range)

library(ggplot2)
qplot(data = reddit, x = age.range)
