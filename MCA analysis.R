dfs=singapore_complete
dfs1=subset(dfs,select=-c(`Membership Id`,`Membership Last Purchase Date`,`Membership Total Purchase Amount`,`Membership Total Discount Amount`,
                   Sales))
View(dfs1)

dfs1$Brand=as.factor(dfs1$Brand)
dfs1$`Reg Tx Division`=as.factor(dfs1$`Reg Tx Division`)
dfs1$`Membership Tier`=as.factor(dfs1$`Membership Tier`)
dfs1$`Purchase Frequency`=as.factor(dfs1$`Purchase Frequency`)
dfs1$`Age Range`=as.factor(dfs1$`Age Range`)
dfs1$`Preferred Language`=as.factor(dfs1$`Preferred Language`)
dfs1$Gender=as.factor(dfs1$Gender)

dfs4=subset(dfs1,select=-c(Brand))

summary(dfs4)
levels(dfs1$Brand)
sapply(dfs1,levels)

res1=MCA(dfs2)
dim(dfs2)
dfs2=distinct(dfs1)

eigen_values=get_eigenvalue(res1)
head(round(eigen_values,2))
fviz_screeplot(res1)
fviz_mca_biplot(res1)+theme_minimal()


var=get_mca_var(res1)
var
plot(res1,choix="var")
fviz_mca_var(res1)
fviz_mca_var(res1, col.var="black", shape.var = 20)

categories <- rownames(var$coord)
length(categories)
glimpse(categories)
View(categories)


res2=MCA(dfs5)
dfs5=distinct(dfs4)
egval=get_eigenvalue(res2)
head(round(egval,2))
fviz_screeplot(res2)
fviz_mca_biplot(res2)+theme_minimal()


var2=get_mca_var(res2)
var2
fviz_mca_var(res2)
fviz_mca_var(res2, col.var="black", shape.var = 0.05)
categories1 <- rownames(var2$coord)
length(categories1)
glimpse(categories1)
View(categories1)
