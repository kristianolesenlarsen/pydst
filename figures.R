library(ggplot2)


NAN1 = read.csv("NAN1.csv", sep = ";")


fixedPrice = subset(NAN1, PRISENHED = "2010-prices- chained values- (bill. dkk.)")

fixedPrice[1:4,]

ggplot(data = fixedPrice) +
   geom_point(aes(x = as.numeric(TID), y = as.numeric(INDHOLD)))
