### Association Pattern Analysis
spore=read_csv("spore.csv")

others=spore%>%filter(Category!="Wine_Spirits")
wines=spore%>%filter(Category=="Wine_Spirits")
dfo=wines
dfo$`Membership Last Purchase Date`=as.Date(dfo$`Membership Last Purchase Date`,format="%d-%m-%Y")
glimpse(dfo$`Membership Last Purchase Date`)
dfo$`Membership Id`=as.character(dfo$`Membership Id`)

# Extracting month and year from date column
dfo=dfo%>%mutate(Yr=lubridate::year(`Membership Last Purchase Date`))%>%filter(Yr==c(2017))
dfo=dfo%>%mutate(mnth=lubridate::month(`Membership Last Purchase Date`,label=T))
View(dfo)
dfo$Yr=NULL;dfo$Wine_Spirits=NULL;dfo$Accessories=NULL;dfo$Watches_Jewelery=NULL;dfo$`Food&Gifts`=NULL;dfo$Fashion_Accessories=NULL;dfo$Fashion=NULL;dfo$Beauty_Fragrance=NULL
write_csv(dfo,"winesoc.csv")

# Which month is the most sale of products

dfo%>%ggplot(aes(x=mnth))+geom_histogram(stat = "count",fill="indianred")

# Top 10 bestsellers

detach("package:plyr", unload=TRUE)

tm=dfo%>%group_by(Brand)%>%summarise(count=n())%>%arrange(desc(count))
tm=head(tm)
tm

tm%>%ggplot(aes(x=reorder(Brand,count),y=count))+geom_bar(stat="identity",fill="indianred")+coord_flip()

dfo$`Membership Id`=as.numeric(as.character(dfo$`Membership Id`))

dfos=dfo[order(dfo$`Membership Id`),]
library(plyr)
itl=ddply(dfo,c("`Membership Id`","`Membership Last Purchase Date`"),function(df1)paste(df1$Brand,collapse = ","))

View(itl)

itl$`Membership Id`=NULL
itl$`Membership Last Purchase Date`=NULL
colnames(itl)=c("items")

## Write the items datframe in csv file

write_csv(itl,"wines_basket.csv")

###### Read Transactions.csv

tr=read.transactions('wines_basket.csv',format='basket',sep = ",",quote = "",skip=1)
summary(tr)
inspect(tr[1:5])
itemFrequencyPlot(tr, topN=20)

### Creating rules

rules <- apriori(tr, parameter = list(supp=0.0005,confidence=0.8))
rules <- sort(rules, by='confidence', decreasing = TRUE)
redundant <- which (colSums (is.subset (rules, rules)) > 1)
length(redundant)
rules=rules[-redundant]
summary(rules)
inspectDT(rules)

plot(rules,method="graph",shading = "confidence")

### Understanding what lead to one product
rules1 <- apriori (data=tr, parameter=list (supp=0.0005,conf = 0.01), appearance = list (default="lhs",rhs="Bacardi"), control = list (verbose=F)) 
inspectDT(rules1)

### Understanding what other products were bought after buying one product
rules2 <- apriori (data=tr, parameter=list (supp=0.0001,conf = 0.01,minlen=2), appearance = list (default="rhs",lhs="Heineken"), control = list (verbose=F))
inspectDT(rules2)
