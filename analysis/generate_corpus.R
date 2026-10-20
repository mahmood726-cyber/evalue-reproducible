source("analysis/versions.R")
assert_versions(c("metadat", "metafor"))
args <- commandArgs(trailingOnly=TRUE)
destination <- if(length(args)) args[[1]] else "data/real-corpus.csv"
options(digits=17)
rows <- list()
add <- function(id, dataset, row, measure, point, lo, hi, rare=FALSE) {
  stopifnot(all(is.finite(c(point, lo, hi))), lo <= point, point <= hi)
  rows[[length(rows)+1L]] <<- data.frame(id, dataset, row, measure, point, lo, hi, rare)
}
bcg <- metadat::dat.bcg
stopifnot(all(c("tpos","tneg","cpos","cneg") %in% names(bcg)))
for(measure in c("RR","OR")) {
  e <- metafor::escalc(measure=measure, ai=tpos, bi=tneg, ci=cpos, di=cneg,
                       data=bcg, add=0.5, to="only0")
  for(i in seq_len(nrow(e))) {
    ci <- exp(e$yi[i] + c(-1,1)*qnorm(.975)*sqrt(e$vi[i]))
    for(rare in if(measure=="OR") c(FALSE,TRUE) else FALSE)
      add(sprintf("bcg-%02d-%s-%s",i,measure,rare), "metadat::dat.bcg", i,
          measure, exp(e$yi[i]), ci[1], ci[2], rare)
  }
}
normand <- metadat::dat.normand1999
stopifnot(all(c("m1i","sd1i","n1i","m2i","sd2i","n2i") %in% names(normand)))
e <- metafor::escalc(measure="SMD", m1i=m1i, sd1i=sd1i, n1i=n1i,
                     m2i=m2i, sd2i=sd2i, n2i=n2i, vtype="LS", data=normand)
for(i in seq_len(nrow(e))) {
  ci <- e$yi[i] + c(-1,1)*qnorm(.975)*sqrt(e$vi[i])
  add(sprintf("normand-%02d-SMD",i), "metadat::dat.normand1999", i,
      "SMD", e$yi[i], ci[1], ci[2])
}
out <- do.call(rbind, rows)
stopifnot(!anyDuplicated(out$id))
dir.create(dirname(destination), recursive=TRUE, showWarnings=FALSE)
write.csv(out, destination, row.names=FALSE, na="")
write.csv(bcg, file.path(dirname(destination),"dat.bcg.csv"), row.names=FALSE)
write.csv(normand, file.path(dirname(destination),"dat.normand1999.csv"), row.names=FALSE)
cat(nrow(out), "real-data configurations generated; these are inputs, not EValue validation results\n")
