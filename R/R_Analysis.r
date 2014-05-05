# 1. Distribution of Expense
exp = as.matrix(read.csv("/Users/RieK/IHK2/Data/Rural_mmrp_list3.csv"))
par(mfrow=c(1,2))
hist(exp, breaks=20, xlab="MPCE", main="Distribution of MPCE", col="royalblue1")
plot(density(exp), xlab="MPCE", main="MPCE Distibution Density", col = "orangered3")

#test run for Andhra Pradesh state
mpceTest = read.csv("/Users/RieK/IHK2/Data/andhra_pradesh_mpce.csv") # column vector data
ruralMpce= mpceTest[,1]
urbanMpce= mpceTest[,2] # it needs to be row vector
ruralData = log(ruralMpce) # take log of each value
urbanData = log(urbanMpce)

simMpceRural = rlnorm(2000, mean(ruralData), sd(ruralData)) 
simMpceUrban = rlnorm(2000, mean(urbanData), sd(urbanData)) 

### graphics for simulated mpce ###
par(mfrow=c(1,2))
hist(simMpceRural, xlab="Rural MPCE", breaks=20, main="Simulated Andhra Pradesh (Rural)", col="palegreen3")
abline(v=mean(simMpceRural), col="red", lwd=2)
msg1 = paste("true mean = ", round(mean(ruralMpce),2), sep="")
msg2 = paste("sim mean = ", round(mean(simMpceRural),2), sep="")
msg3 = paste("true sd = ", round(sd(ruralMpce),2), sep="")
msg4 = paste("sim sd = ", round(sd(simMpceRural),2), sep="")
legend('topright', c(msg1,msg2,msg3,msg4), text.col = c("gray45", "blue"), bty='n', cex=0.5)

hist(simMpceUrban, xlab="Urban MPCE", breaks=20, main="Simulated Andhra Pradesh (Urban)", col="orchid1")
abline(v=mean(simMpceUrban), col="red", lwd=2)
msg1 = paste("true mean = ", round(mean(urbanMpce),2), sep="")
msg2 = paste("sim mean = ", round(mean(simMpceUrban),2), sep="")
msg3 = paste("true sd = ", round(sd(urbanMpce),2), sep="")
msg4 = paste("sim sd = ", round(sd(simMpceUrban),2), sep="")
legend('topright', c(msg1,msg2,msg3,msg4), text.col = c("gray45", "blue"), bty='n', cex=0.5)

### diraphics for simulated expenditure ###
par(mfrow=c(1,2))
hist(simulatedMPCE, xlab="Simulated MPCE", breaks=20, main="Simulated MPCE", col="palegreen3")
abline(v=mean(simulatedMPCE), col="red", lwd=2)
msg1 = paste("mean = ", round(mean(simPoor),2), sep="")
msg2 = paste("sd = ", round(sd(simPoor),2), sep="")
legend('topright', c(msg1,msg2), text.col = "blue", bty='n', cex=0.5)

# 2. Distribution of Income

income = read.csv("/Users/RieK/IHK2/Data/gsp.csv")
income = sort(t(income))
poor = income[1:12]
rich = income[13:length(income)]
poorLog = log(poor)
richLog = log(rich)
simPoor = rlnorm(2000, mean(poorLog), sd(poorLog))
simRich = rlnorm(2000, mean(richLog), sd(richLog))
hist(simPoor)
hist(simRich)
mean(poor)
mean(simPoor)
sd(poor)
sd(simPoor)

mean(rich)
mean(simRich)
sd(rich)
sd(simRich)
### for income distribution graph ###
income = read.csv("/Users/RieK/IHK2/Data/gsp.csv")
income = sort(t(income))
par(mfrow=c(1,2))
hist(income, breaks=20, xlab="GSP", main="GSP Distibution", col="royalblue1")
plot(density(income), xlab="GSP", main="GSP Distibution Density", col = "orangered3")
### for simulated distribution graph ###
par(mfrow=c(1,2))
hist(simPoor, xlab="Poor-State GSP", breaks=20, main="Simulated Poor-State", col="palegreen3")
abline(v=mean(simPoor), col="red", lwd=2)
msg1 = paste("mean = ", round(mean(simPoor),2), sep="")
msg2 = paste("sd = ", round(sd(simPoor),2), sep="")
legend('topright', c(msg1,msg2), text.col = "blue", bty='n', cex=0.5)

hist(simRich, xlab="Rich-State GSP", breaks=20, main="Simulated Rich-State", col="orchid1")
abline(v=mean(simRich), col="red", lwd=2)
msg3 = paste("mean = ", round(mean(simRich),2), sep="")
msg4 = paste("sd = ", round(sd(simRich),2), sep="")
legend('topright', c(msg3,msg4), text.col = "blue", bty='n', cex=0.5)

#3. Distribution of Genders

gender = read.csv("/Users/RieK/IHK2/Data/sex.csv")
femalePercentage = mean (gender$F) # 0.4882624
malePercentage = mean (gender$M) # 0.5117376

# Distribution of Age
age = read.csv("/Users/RieK/IHK2/Data/age.csv")
ruralAge=age[22,2:7]
urbanAge=age[22,8:13]

### combined pie chart for Gender and Age ###

### for gender pie chart ###
sliceGen <- c(femalePercentage, malePercentage)
lbGen <- c("Female:", "Male:")
pctGen <- round(sliceGen, 4) * 100
lbGen <- paste(lbGen, pctGen)
lbGen <- paste(lbGen,"%",sep="")
sliceAge1 = c(19.1,20.7,33.1,18.8,7.6,0.8)
lbAge <- c("< 10: ", "10-19: ", "20-39: ", "40-59: ", "60-79: ", "> 80: ")
lbAge1 = paste(lbAge, sliceAge1, sep="")
lbAge1 = paste(lbAge1, "%", sep="")
sliceAge2 = c(16.3,18.3,35.9,21.5,7.3,0.7)
lbAge2 = paste(lbAge, sliceAge2, sep="")
lbAge2 = paste(lbAge2, "%", sep="")
par(mfrow=c(1,3))
pie(sliceGen, labels = lbGen, col=c("hotpink1", "deepskyblue2"),main="Gender Weight")
pie(sliceAge1, labels = lbAge1, col=rainbow(length(lbAge1)),main="Age Weight - Rural")
pie(sliceAge2, labels = lbAge2, col=rainbow(length(lbAge2)),main="Age Weight - Urban")

# Distribution of Eye-sight
par(mfrow=c(1,1))
eye = rnorm(1000, 1.5, (0.6))
# hist(eye, xlim=c(-0.5,2), col="darkorange1", breaks=40)
plot(density(eye), xlim=c(-0.5,2), col="darkorange1", xlab="Eye Utility", main="Truncated Density of Eye Utility")
polygon(density(eye), col="darkorange1", border=FALSE)
legend('topleft', "truncated mean = 0.8518", text.col = "blue", bty='n', cex=1)
abline(v=0, col="red", lwd=2)
abline(v=1, col="red", lwd =2)

# Health Data
health= read.csv("/Users/RieK/IHK2/Data/health.csv")
X = matrix( c(rep(1,28), health[,4], health[,5], health[,6]), ncol = 4 )
Y = health[,3]
Beta = solve( t(X) %*% X ) %*% t(X) %*% Y
Beta
# [Intercept,]  -0.0001009257
# [Education,]  -0.9997093899
# [Income,]     -0.9931986439
# [Gender.Dev,]  2.9921899757

# QALY improvement
true.mean = 1.621
qaly= as.matrix(read.csv("/Users/RieK/IHK/qaly_improvement.csv"))
den = density(qaly)
myhist = hist(qaly, main = "1,000 Replications of QALY Change", border=FALSE,col = "limegreen")
abline(v=mean(qaly),col="red",lwd=2)
msg1 = paste("Mean QALY Change: ",round(mean(qaly),digit=5),sep="")
msg2 = paste("SD QALY Change: ",round(sd(qaly),digit=5),sep="")
z = round( (mean(qaly) - true.mean) / sd(qaly), digit=4)
msg3 = paste("Z-Score: ", z, sep="")
legend("topright", c(msg1,msg2,msg3), text.col="red",bty='n',cex=1)
multiplier = myhist$counts / myhist$density
den$y = den$y * multiplier[1]
lines(den, col = "blue")


