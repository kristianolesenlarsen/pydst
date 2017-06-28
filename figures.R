#possibly deprecated

library(readr)
library(tidyverse)
library(viridis)

NAN1 = read.csv("NAN1.csv", sep = ";")

#%>%
#  mutate(INDHOLD = as.numeric(INDHOLD))

fixedPrice = subset(NAN1, PRISENHED == "2010-prices- chained values- (bill. dkk.)" | PRISENHED == "Period-to-period real growth in per cent") %>%
             subset(TRANSAKT == "B.1*g Gross domestic product") %>%
             spread(PRISENHED, INDHOLD) %>%
             set_colnames(c("TRANSAKT","TID","CHAINED","CHANGE"))


fixedPrice

fixedPrice$CHANGE= as.numeric(as.character(fixedPrice$CHANGE))
fixedPrice$CHAINED= as.numeric(as.character(fixedPrice$CHAINED))

ggplot(data = fixedPrice) +
   geom_smooth(aes(x = as.numeric(TID), y = as.numeric(CHAINED)), size = 0.4, color = "grey") +
   geom_line(aes(x = as.numeric(TID), y = as.numeric(CHAINED)))
