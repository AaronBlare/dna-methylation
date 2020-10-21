rm(list=ls())

if (!requireNamespace("BiocManager", quietly=TRUE))
  install.packages("BiocManager")
BiocManager::install("ChAMP")

library("ChAMP")

path <- "E:/YandexDisk/Work/pydnameth/unn_epic/raw/release"
setwd(path)

myImport = champ.import(directory = path, arraytype = "EPIC")

beta_raw = myImport$beta
write.table(data.frame(beta_raw),file="beta_raw.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

myLoad <- champ.filter(arraytype = "EPIC")

champ.QC()

QC.GUI(beta=myLoad$beta,arraytype="EPIC")

myNorm <- champ.norm(arraytype = "EPIC", plotBMIQ = TRUE)

champ.QC(beta = myNorm,
         pheno=myLoad$pd$Sample_Group,
         mdsPlot=TRUE,
         densityPlot=TRUE,
         dendrogram=TRUE,
         PDFplot=TRUE,
         Rplot=TRUE,
         Feature.sel="None",
         resultsDir="./CHAMP_QCimages_normed/")

QC.GUI(beta=myNorm,arraytype="EPIC")

beta_filtered_normalized = myNorm
write.table(data.frame(beta_filtered_normalized),file="beta_filtered_normalized.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

#write.table(data.frame(EPIC.manifest.hg19),file="EPIC.manifest.hg19.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

champ.SVD(beta=myNorm,pd=myLoad$pd)

myCombat <- champ.runCombat(beta=myNorm, pd=myLoad$pd, batchname=c("Slide"))

write.table(data.frame(beta_filtered_normalized),file="beta_filtered_normalized_combat.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)





if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("minfi")
BiocManager::install("FlowSorted.Blood.EPIC")


library(minfi)
library(FlowSorted.Blood.EPIC)


# ====== File system =======
path <- "E:/YandexDisk/Work/pydnameth/unn_epic/raw/release"
setwd(path)
# ==========================

# ======= RGset ========
list.files(path)
targets <- read.metharray.sheet(path)
RGset <- read.metharray.exp(targets = targets)

cell_counts <- estimateCellCounts2(RGset, referencePlatform="IlluminaHumanMethylationEPIC")






rm(list=ls())

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("minfi")
BiocManager::install("minfiData")
BiocManager::install("wateRmelon")
BiocManager::install("shinyMethyl")
BiocManager::install("FlowSorted.Blood.EPIC")

library(minfi)
library(minfiData)
library(shinyMethyl)
library(wateRmelon)
library(FlowSorted.Blood.EPIC)


# ====== File system =======
path <- "E:/YandexDisk/Work/pydnameth/unn_epic/raw/release"
setwd(path)
# ==========================

# ======= RGset ========
list.files(path)
targets <- read.metharray.sheet(path)
RGset <- read.metharray.exp(targets = targets)

manifest <- getManifest(RGSet)
# ======================


# ======= Control probes ========
df_TypeControl <- data.frame(getProbeInfo(RGset, type = "Control"))
pdf("control_negative.pdf",width=15,height=5)
controlStripPlot(RGset, controls="NEGATIVE")
dev.off()
# ===============================

# ======= shinyMethyl =======
summary <- shinySummarize(RGset)
save(summary,file="summary_shinyMethyl.RData")
# ===========================

# ========= pfilter ===========
wateRmelon_filtered <- pfilter(RGset, pnthresh=0.05, perc=5, pthresh=1)
# =============================

# ======== Processing with filtering =========
MSet_raw <- preprocessRaw(RGset)
green <- getGreen(RGset)
red <- getRed(RGset)
beta_raw <- getBeta(RGset)

pdf("boxplots_intensities.pdf", width=15, height=5)
par(mfrow=c(3,1))
boxplot(green,outline=F)
boxplot(red,outline=F)
boxplot(beta_raw,outline=F)
dev.off()

qc <- getQC(MSet_raw)
pdf("QCplot.pdf")
plotQC(qc)
plotQC(qc, badSampleCutoff = 10.5)
dev.off()

pdf("boxplots_beta_Raw.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_raw,outline=F,main="No Normalization")
dev.off()

detP <- detectionP(RGset)
failed <- detP>0.05
means_of_columns <- colMeans(failed) 
means_of_columns
samples_to_retain <- means_of_columns<0.05
names_samples_to_remove <- names(samples_to_retain)[samples_to_retain==FALSE]
length(names_samples_to_remove)
names_samples_to_remove

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
beta_filtered_samples <- beta_filtered_samples[!rownames(beta_filtered_samples) %in% names_probes_to_remove,]
dim(beta_filtered_samples)

funnorm <- preprocessFunnorm(RGset_filtered_samples)
beta_funnorm <- getBeta(funnorm)
beta_funnorm <- beta_funnorm[!rownames(beta_funnorm) %in% names_probes_to_remove,]
dim(beta_funnorm)
pdf("boxplots_beta_Raw_filtered_samples_probes.pdf",width=20,height=10)
par(mfrow=c(1,1))
boxplot(beta_filtered_samples,outline=F,main="No Normalization")
dev.off()
pdf("boxplots_beta_Funnorm_filtered_samples_probes.pdf",width=20,height=10)
par(mfrow=c(1,1))
boxplot(beta_funnorm,outline=F,main="Funnorm Normalization")
dev.off()

beta_funnorm <- data.frame(row.names(beta_funnorm),beta_funnorm)
colnames(beta_funnorm)[1] <- "ID_REF"
dim(beta_funnorm)
str(beta_funnorm)
getwd()
save(beta_funnorm,file="beta_Funnorm_filtered_samples_probes.RData")
write.table(beta_funnorm,file="beta_Funnorm_filtered_samples_probes.txt",row.names=F,sep="\t",quote=F)

quantile <- preprocessQuantile(RGset_filtered_samples)
beta_quantile <- getBeta(quantile)
beta_quantile <- beta_quantile[!rownames(beta_quantile) %in% names_probes_to_remove,]
dim(beta_quantile)
pdf("boxplots_beta_Quantile_filtered_samples_probes.pdf",width=20,height=10)
par(mfrow=c(1,1))
boxplot(beta_quantile,outline=F,main="quantile Normalization")
dev.off()

beta_quantile <- data.frame(row.names(beta_quantile),beta_quantile)
colnames(beta_quantile)[1] <- "ID_REF"
dim(beta_quantile)
str(beta_quantile)
getwd()
save(beta_quantile,file="beta_Quantile_filtered_samples_probes.RData")
write.table(beta_funnorm,file="beta_Quantile_filtered_samples_probes.txt",row.names=F,sep="\t",quote=F)
# ===============================

# ======== preprocessFunnorm =========
funnorm <- preprocessFunnorm(RGset)
beta_funnorm <- getBeta(funnorm)
dim(beta_funnorm)
pdf("boxplots_beta_Funnorm.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_funnorm,outline=F,main="Funnorm Normalization")
dev.off()

beta_funnorm <- data.frame(row.names(beta_funnorm),beta_funnorm)
colnames(beta_funnorm)[1] <- "ID_REF"
save(beta_funnorm,file="beta_funnorm.RData")
write.table(beta_funnorm,file="beta_funnorm.txt",row.names=F,sep="\t",quote=F)
rm(beta_funnorm)
# ====================================


# ======== preprocessQuantile =========
quantile <- preprocessQuantile(RGset)
beta_quantile <- getBeta(quantile)
dim(beta_quantile)
pdf("boxplots_beta_Quantile.pdf",width=15,height=5)
par(mfrow=c(1,1))
boxplot(beta_quantile,outline=F,main="Quantile Normalization")
dev.off()

beta_quantile <- data.frame(row.names(beta_quantile),beta_quantile)
colnames(beta_quantile)[1] <- "ID_REF"
save(beta_quantile,file="beta_quantile.RData")
write.table(beta_quantile,file="beta_quantile.txt",row.names=F,sep="\t",quote=F)
rm(beta_quantile)
# ====================================




