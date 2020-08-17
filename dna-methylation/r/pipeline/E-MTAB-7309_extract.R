rm(list=ls())
library(minfi)
baseDir <- ("/home/PERSONALE/mariagiuli.bacalini2/E-MTAB-7309/Input_data")
list.files(baseDir)
targets <- read.metharray.sheet(baseDir)
targets
RGset <- read.metharray.exp(targets = targets)
RGset
setwd("/home/PERSONALE/mariagiuli.bacalini2/E-MTAB-7309/")
save(RGset,file="E-MTAB-7309_RGset.RData")
load("E-MTAB-7309_RGset.RData")
getwd()

# source("https://bioconductor.org/biocLite.R")
# biocLite("FlowSorted.Blood.450k")

# CellCounts <- estimateCellCounts(RGset)
# save(CellCounts,file="E-MTAB-7309_CellCounts.RData")
# load("E-MTAB-7309_CellCounts.RData")
# ls()
# head(CellCounts)
# list.files()

MSet_Raw <- preprocessRaw(RGset)

green <- getGreen(RGset)
red <- getRed(RGset)
beta <- getBeta(RGset)

pdf("E-MTAB-7309_boxplots_intensities.pdf",width=15,height=5)
par(mfrow=c(3,1))
boxplot(green,outline=F)
boxplot(red,outline=F)
boxplot(beta,outline=F)
dev.off()

# Controlli di qualità
# qcplot
qc <- getQC(MSet_Raw)
pdf("E-MTAB-7309_QCplot.pdf")
plotQC(qc)
dev.off()

# Detection pValue
detP <- detectionP(RGset)
failed <- detP>0.05
means_of_columns <- colMeans(failed) 
means_of_columns
samples_to_retain <- means_of_columns<0.05
names_samples_to_remove <- names(samples_to_retain)[samples_to_retain==FALSE]
length(names_samples_to_remove)
names_samples_to_remove
# [1] "9721365034_R06C01" "9721365047_R06C01" "9721365190_R01C02"
# [4] "9721365029_R03C01" "9721365076_R06C02" "9721365033_R03C01"
# [7] "9721365146_R04C01" "9721365092_R01C02" "9721365035_R04C02"
# [10] "9721365003_R06C01" "9721365003_R02C02" "9721365088_R01C02"
# [13] "9721365007_R04C01"

means_of_rows <- rowMeans(failed)
probes_to_retain <- means_of_rows<0.01
names_probes_to_remove <- names(probes_to_retain)[probes_to_retain==FALSE]
length(names_probes_to_remove)

RGset_filtered_samples <- RGset[, samples_to_retain]
RGset_filtered_samples

detP_filtered_samples <- detectionP(RGset_filtered_samples)
failed_filtered_samples <- detP_filtered_samples>0.05
means_of_rows <- rowMeans(failed_filtered_samples)
probes_to_retain <- means_of_rows<0.01
names_probes_to_remove <- names(probes_to_retain)[probes_to_retain==FALSE]
length(names_probes_to_remove)

MSet_Raw_filtered_samples <- preprocessRaw(RGset_filtered_samples)
beta_filtered_samples <- getBeta(MSet_Raw_filtered_samples)

funnorm <- preprocessFunnorm(RGset_filtered_samples)
beta_funnorm <- getBeta(funnorm)
beta_funnorm <- beta_funnorm[!rownames(beta_funnorm) %in% names_probes_to_remove,]
dim(beta_funnorm)
pdf("E-MTAB-7309_boxplots_beta_Funnorm_filtered_samples_probes.pdf",width=20,height=5)
par(mfrow=c(2,1))
boxplot(beta,outline=F,main="No Normalization")
boxplot(beta_funnorm,outline=F,main="Funnorm Normalization")
dev.off()

beta_funnorm <- data.frame(row.names(beta_funnorm),beta_funnorm)
colnames(beta_funnorm)[1] <- "ID_REF"
dim(beta_funnorm)
str(beta_funnorm)
getwd()
save(beta_funnorm,file="E-MTAB-7309_beta_Funnorm_filtered_samples_probes.RData")

rm(funnorm)
rm(beta_funnorm)

quantile <- preprocessQuantile(RGset_filtered_samples)
beta_quantile <- getBeta(quantile)
beta_quantile <- beta_quantile[!rownames(beta_quantile) %in% names_probes_to_remove,]
dim(beta_quantile)
pdf("E-MTAB-7309_boxplots_beta_Quantile_filtered_samples_probes.pdf",width=20,height=5)
par(mfrow=c(2,1))
boxplot(beta,outline=F,main="No Normalization")
boxplot(beta_quantile,outline=F,main="quantile Normalization")
dev.off() 

beta_quantile <- data.frame(row.names(beta_quantile),beta_quantile)
colnames(beta_quantile)[1] <- "ID_REF"
dim(beta_quantile)
str(beta_quantile)
getwd()
save(beta_quantile,file="E-MTAB-7309_beta_Quantile_filtered_samples_probes.RData")



write.table(beta_funnorm,file="E-MTAB-7309_beta_funnorm.txt",row.names=F,sep="\t",quote=F)
write.table(beta_quantile,file="E-MTAB-7309_beta_quantile.txt",row.names=F,sep="\t",quote=F)
