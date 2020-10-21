rm(list=ls())

if (!requireNamespace("BiocManager", quietly=TRUE))
  install.packages("BiocManager")
BiocManager::install("ChAMP")

library("ChAMP")

path <- "E:/YandexDisk/Work/pydnameth/script_datasets/GPL21145/test_single/GSE123914/raw_data"
setwd(path)

myImport = champ.import(directory = path, arraytype = "EPIC")

beta_raw = myImport$beta
write.table(data.frame(beta_raw),file="beta_raw.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

myLoad <- champ.filter(arraytype = "EPIC")

champ.QC()

QC.GUI(beta=myLoad$beta,arraytype="EPIC")

myNorm <- champ.norm(arraytype = "EPIC", plotBMIQ = TRUE)

beta_filtered_normalized = myNorm
write.table(data.frame(beta_filtered_normalized),file="beta_filtered_normalized.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

write.table(data.frame(EPIC.manifest.hg19),file="EPIC.manifest.hg19.txt",col.name=TRUE, row.names=TRUE,sep="\t",quote=F)

champ.SVD(beta=myNorm,pd=myLoad$pd)

myCombat <- champ.runCombat(beta=myNorm, pd=myLoad$pd, batchname=c("Slide"))
