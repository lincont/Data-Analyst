<<<<<<< HEAD
## Introduction to R, using pretend facebook data


## find your current directory
getwd()

## change the directory
setwd('../Downloads')

## get a listing of the files
list.files()

## load data into a dataframe called pf
pf <- read.csv('pseudo_facebook.tsv', sep = '\t')

## load the viz library
library(ggplot2)

## what are our data columns
names(pf)

## plot dob by day 1 - 31
qplot(x= dob_day, data = pf) + 
  scale_x_continuous(breaks=1:31)

## plot by gender
qplot(x = friend_count, data = pf, binwidth = 25) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)

## omitting null genders
qplot(x = friend_count, data = subset(pf, !is.na(gender)), binwidth = 25) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)

## remove all nulls in the entire dataset, be careful with this one
qplot(x = friend_count, data = na.omit(pf), binwidth = 25) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)

## stats by gender
table(pf$gender)
by(pf$friend_count, pf$gender, summary)

## examples of making it pretty, tenure in days
ggplot(aes(x = tenure), data = pf) +
  geom_histogram(binwidth = 30, color = 'black', fill = '#099DD9')

ggplot(aes(x = tenure/365), data = pf) +
  geom_histogram(binwidth = .25, color = 'black', fill = '#F79420') +
  scale_x_continuous(breaks = seq(1, 7, 1), limits = c(0, 7))

## example of age using ggplot
ggplot(aes(x = age), data = pf) +
  geom_histogram(binwidth = 1, fill = '#5760AB') +
  scale_x_continuous(breaks = seq(0, 113, 5))

## exploring age using qplot
qplot(x = age, data = pf)

## exploring age and making it pretty using qplot
qplot(x = age, data = pf, binwidth = 1, fill = I('#5760AB')) +
  scale_x_continuous(breaks = seq(0, 113, 5))

# example 1 of plotting three histograms on one view
install.packages('gridExtra')
library(gridExtra)

p1 <- qplot(x = friend_count, data=pf)
p2 <- qplot(x = log10(friend_count + 1), data = pf)
p3 <- qplot(x = sqrt(friend_count), data = pf)

grid.arrange(p1, p2, p3, ncol=1)

# example 2 of plotting three histograms on one view
p1 <- ggplot(aes(x = friend_count), data=pf) + geom_histogram()
p2 <- p1 + scale_x_log10()
p3 <- p1 + scale_x_sqrt()

grid.arrange(p1, p2, p3, ncol=1)


## Frequency Plot example using qgplot
qplot(x=friend_count, data = subset(pf, !is.na(gender)),
      binwidth = 10) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)

qplot(x = friend_count, y = ..count../sum(..count..),
       data = subset(pf, !is.na(gender)),
  xlab('Friend Count'),
  ylab('Proportion of users with that friend count'),
  binwidth = 10, geom = 'freqpoly', color = gender) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50))

## Frequency Plot example using ggplot
ggplot(aes(x = friend_count), data = subset(pf, !is.na(gender))) +
  geom_freqpoly(aes(color = gender)) +
  scale_x_log10()

ggplot(aes(x = friend_count, y = ..count../sum(..count..)),
       data = subset(pf, !is.na(gender))) +
  geom_freqpoly(aes(color = gender), binwidth=10) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  xlab('Friend Count') +
  ylab('Proportion of users with that friend count')


ggplot(aes(x = www_likes), data = subset(pf, !is.na(gender))) +
  geom_freqpoly(aes(color = gender)) +
  scale_x_log10()

## sum the www_likes by gender
by(pf$www_likes, pf$gender, sum)

## experiment with boxplots
qplot (x=gender, y=friend_count, 
       data = subset(pf, !is.na(gender)), 
       geom = 'boxplot', ylim = c(0, 1000))

qplot (x=gender, y=friend_count, 
       data = subset(pf, !is.na(gender)), 
       geom = 'boxplot') +
  scale_y_continuous(limits = c(0, 1000))

# both of the above will remove data points a better way to scale is to use the below
qplot (x=gender, y=friend_count, 
       data = subset(pf, !is.na(gender)), 
       geom = 'boxplot') +
  coord_cartesian(ylim = c(0, 1000))

# examine more closely
qplot (x=gender, y=friend_count, 
       data = subset(pf, !is.na(gender)), 
       geom = 'boxplot') +
  coord_cartesian(ylim = c(0, 250))

by(pf$friend_count, pf$gender, summary)


## percentages
summary(pf$mobile_likes_received)
=======
## Introduction to R, using pretend facebook data


## find your current directory
getwd()

## change the directory
setwd('../Downloads')

## get a listing of the files
list.files()

## load data into a dataframe called pf
pf <- read.csv('pseudo_facebook.tsv', sep = '\t')

## load the viz library
library(ggplot2)

## what are our data columns
names(pf)

## plot dob by day 1 - 31
qplot(x= dob_day, data = pf) + 
  scale_x_continuous(breaks=1:31)

## plot by gender
qplot(x = friend_count, data = pf, binwidth = 25) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)

## omitting null genders
qplot(x = friend_count, data = subset(pf, !is.na(gender)), binwidth = 25) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)

## remove all nulls in the entire dataset, be careful with this one
qplot(x = friend_count, data = na.omit(pf), binwidth = 25) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)

## stats by gender
table(pf$gender)
by(pf$friend_count, pf$gender, summary)

## examples of making it pretty, tenure in days
ggplot(aes(x = tenure), data = pf) +
  geom_histogram(binwidth = 30, color = 'black', fill = '#099DD9')

ggplot(aes(x = tenure/365), data = pf) +
  geom_histogram(binwidth = .25, color = 'black', fill = '#F79420') +
  scale_x_continuous(breaks = seq(1, 7, 1), limits = c(0, 7))

## example of age using ggplot
ggplot(aes(x = age), data = pf) +
  geom_histogram(binwidth = 1, fill = '#5760AB') +
  scale_x_continuous(breaks = seq(0, 113, 5))

## exploring age using qplot
qplot(x = age, data = pf)

## exploring age and making it pretty using qplot
qplot(x = age, data = pf, binwidth = 1, fill = I('#5760AB')) +
  scale_x_continuous(breaks = seq(0, 113, 5))

# example 1 of plotting three histograms on one view
install.packages('gridExtra')
library(gridExtra)

p1 <- qplot(x = friend_count, data=pf)
p2 <- qplot(x = log10(friend_count + 1), data = pf)
p3 <- qplot(x = sqrt(friend_count), data = pf)

grid.arrange(p1, p2, p3, ncol=1)

# example 2 of plotting three histograms on one view
p1 <- ggplot(aes(x = friend_count), data=pf) + geom_histogram()
p2 <- p1 + scale_x_log10()
p3 <- p1 + scale_x_sqrt()

grid.arrange(p1, p2, p3, ncol=1)


## Frequency Plot example using qgplot
qplot(x=friend_count, data = subset(pf, !is.na(gender)),
      binwidth = 10) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  facet_wrap(~gender)

qplot(x = friend_count, y = ..count../sum(..count..),
       data = subset(pf, !is.na(gender)),
  xlab('Friend Count'),
  ylab('Proportion of users with that friend count'),
  binwidth = 10, geom = 'freqpoly', color = gender) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50))

## Frequency Plot example using ggplot
ggplot(aes(x = friend_count), data = subset(pf, !is.na(gender))) +
  geom_freqpoly(aes(color = gender)) +
  scale_x_log10()

ggplot(aes(x = friend_count, y = ..count../sum(..count..)),
       data = subset(pf, !is.na(gender))) +
  geom_freqpoly(aes(color = gender), binwidth=10) +
  scale_x_continuous(limits = c(0, 1000), breaks = seq(0, 1000, 50)) +
  xlab('Friend Count') +
  ylab('Proportion of users with that friend count')


ggplot(aes(x = www_likes), data = subset(pf, !is.na(gender))) +
  geom_freqpoly(aes(color = gender)) +
  scale_x_log10()

## sum the www_likes by gender
by(pf$www_likes, pf$gender, sum)

## experiment with boxplots
qplot (x=gender, y=friend_count, 
       data = subset(pf, !is.na(gender)), 
       geom = 'boxplot', ylim = c(0, 1000))

qplot (x=gender, y=friend_count, 
       data = subset(pf, !is.na(gender)), 
       geom = 'boxplot') +
  scale_y_continuous(limits = c(0, 1000))

# both of the above will remove data points a better way to scale is to use the below
qplot (x=gender, y=friend_count, 
       data = subset(pf, !is.na(gender)), 
       geom = 'boxplot') +
  coord_cartesian(ylim = c(0, 1000))

# examine more closely
qplot (x=gender, y=friend_count, 
       data = subset(pf, !is.na(gender)), 
       geom = 'boxplot') +
  coord_cartesian(ylim = c(0, 250))

by(pf$friend_count, pf$gender, summary)


## percentages
summary(pf$mobile_likes_received)
>>>>>>> add learning projects
