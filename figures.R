library("ggplot2")
library("tidyverse")
library("zoo")
library("viridis")
library("gganimate")
library("magrittr")

#load shapefile and data
load("municipality.rda")
dat = read.csv("FOLK1A.csv", sep = ";")

dat$TID = as.yearqtr(dat$TID)

dat$OMRÅDE = gsub("æ", "ae", dat$OMRÅDE)
dat$OMRÅDE = gsub("ø", "oe", dat$OMRÅDE)
dat$OMRÅDE = gsub("å", "aa", dat$OMRÅDE)
dat$OMRÅDE = gsub("-", " ", dat$OMRÅDE)
dat$OMRÅDE = tolower(dat$OMRÅDE)

dat$OMRÅDE[dat$OMRÅDE == 'copenhagen'] = "koebenhavn"
dat$OMRÅDE[dat$OMRÅDE == 'æroe'] = "aeroe"

# prepare data
df = dat %>%
#  filter(KØN != "total") %>%
  filter(OMRÅDE != "region hovedstaden") %>%
  filter(OMRÅDE != "all denmark") %>%
  spread(KØN, INDHOLD)


df$Men = as.numeric(df$Men)
df$Women = as.numeric(df$Women)

df = df %>%
  mutate(MF =(Men / Women -1) *100) %>%
  mutate(MF_diff = Men-Women)

# test plot with 1 frame
df_1year = df %>%
  filter(TID == "2017Q2")


ggplot(data = df, aes(frame = TID)) +
  geom_map(aes(map_id = OMRÅDE, fill = MF), map = municipality) +
  expand_limits(x = municipality$long, y = municipality$lat)   +
  scale_fill_gradient2(low = "hotpink", mid = "grey95", high = "blue", name = "Males / Female") +
  coord_quickmap() +
  theme_classic() +
  theme(legend.position = "none", axis.title.y = element_blank(), axis.title.x = element_blank())


#plot for anumation
  p = ggplot(data = df, aes(frame = TID)) +
    geom_map(aes(map_id = OMRÅDE, fill = MF), map = municipality) +
    expand_limits(x = municipality$long, y = municipality$lat)   +
    scale_fill_gradient2(low = "hotpink" , mid = 'grey95', high = "blue") +
    coord_quickmap() +
    theme_classic() +
    theme(legend.position = "bottom", axis.title.y = element_blank(), axis.title.x = element_blank())

  gganimate(p, "test.gif", interval = .2)



## THIS IS NOT AN INTERESTING PLOT
# Plot total population numbers
df2 = dat %>%
  filter(KØN == "Total") %>%
  filter(OMRÅDE != "region hovedstaden") %>%
  filter(OMRÅDE != "all denmark")


p2 = ggplot(data = df2, aes(frame = TID)) +
  geom_map(aes(map_id = OMRÅDE, fill = INDHOLD), map = municipality) +
  expand_limits(x = municipality$long, y = municipality$lat)   +
  scale_fill_gradient(low = "grey95", high = "red", name = "Population") +
  coord_quickmap() +
  theme_classic() +
  theme(legend.position = "none", axis.title.y = element_blank(), axis.title.x = element_blank())

gganimate(p2, "test2.gif", interval = .2)




# Election equality
dat2 = read.csv('LIGEDI0.csv', sep = ";")


df2 = dat2 %>%
  spread(INDIKATOR, INDHOLD) %>%
  set_colnames(c("TID", "KANDIDAT", "MEN", "WOMEN"))


q = ggplot(data = df2, aes(frame = TID, cumulative = TRUE)) +
  geom_line(aes(x = TID, y = MEN, group = KANDIDAT, color = KANDIDAT ), size = 1) +
  geom_line(aes(x = TID, y = WOMEN, group = KANDIDAT, color = KANDIDAT ), size = 1) +
  theme_classic() +
  annotate("text", x = 1910, y = 95, label = "Men") +
  annotate("text", x = 1910, y = 10, label = "Women") +
  theme(legend.position = "top")

gganimate(q,"test3.gif", interval = 0.2)


# moving FROM copenhagen (BORING)

dat3 = read.csv('FLY66.csv', sep = ';')

dat3$TILKOMMUNE = gsub("æ", "ae", dat3$TILKOMMUNE)
dat3$TILKOMMUNE = gsub("ø", "oe", dat3$TILKOMMUNE)
dat3$TILKOMMUNE = gsub("å", "aa", dat3$TILKOMMUNE)
dat3$TILKOMMUNE = gsub("-", " ", dat3$TILKOMMUNE)
dat3$TILKOMMUNE = tolower(dat3$TILKOMMUNE)

dat3$TILKOMMUNE[dat3$TILKOMMUNE == 'copenhagen'] = "koebenhavn"
dat3$TILKOMMUNE[dat3$TILKOMMUNE == 'æroe'] = "aeroe"


z = ggplot(data = dat3, aes(frame = TID)) +
  geom_map(aes(map_id = TILKOMMUNE, fill = INDHOLD), map = municipality) +
  expand_limits(x = municipality$long, y = municipality$lat)   +
  scale_fill_gradient(low = "grey95", high = "green", name = "Population") +
  coord_quickmap() +
  theme_classic() +
  theme(legend.position = "none", axis.title.y = element_blank(), axis.title.x = element_blank())


gganimate(z, interval = 0.2)


#
