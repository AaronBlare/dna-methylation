rm(list=ls())

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")
BiocManager::install("minfi")
BiocManager::install("wateRmelon")
BiocManager::install("shinyMethyl")
BiocManager::install("FlowSorted.Blood.450k")

library(minfi)
library(shinyMethyl)
library(wateRmelon)
library(FlowSorted.Blood.450k)

# ====== Parameters =======
calc_cell_counts = TRUE
control_analysis = FALSE
shinyMethyl_analysis = TRUE
pfilter_analysis = TRUE
raw_analysis = TRUE
funnorm_analysis = TRUE
# =========================

# ====== File system =======
path <- "E:/YandexDisk/Work/pydnameth/script_datasets/GPL13534/filtered/brain(DLPFC)/GSE74193" 
path_to_raw <- paste(path, "/", "raw_data",  sep='')
setwd(path_to_raw)
# ==========================

# ======= RGset ========
RGset_fn <- paste(path_to_raw, "/", "RGset.RData",  sep='')
baseDir <- path_to_raw
list.files(baseDir)
targets <- read.metharray.sheet(baseDir)
RGset <- read.metharray.exp(targets = targets)
save(RGset,file=RGset_fn)
# ======================

# ======= CellCounts ======
if (calc_cell_counts){
  CellCounts_fn <- paste(path_to_raw, "/", "CellCounts.RData",  sep='')
  CellCounts_fn_txt <- paste(path_to_raw, "/", "CellCounts.txt",  sep='')
  if (!file.exists(CellCounts_fn)){
    CellCounts <- estimateCellCounts(RGset)
    save(CellCounts, file=CellCounts_fn)
    write.table(CellCounts, file=CellCounts_fn_txt, row.names=T, sep="\t", quote=F)
  }
  else{
    load(CellCounts_fn)
  }
}
# =========================

# ======= Control probes ========
if (control_analysis){
  df_TypeControl <- data.frame(getProbeInfo(RGset, type = "Control"))
  pdf("control_negative.pdf",width=15,height=5)
  controlStripPlot(RGset, controls="NEGATIVE")
  dev.off()
}
# ===============================

# ======= shinyMethyl =======
if (shinyMethyl_analysis){
  summary <- shinySummarize(RGset)
  save(summary,file="summary_shinyMethyl.RData")
}
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