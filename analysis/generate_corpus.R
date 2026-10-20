source("analysis/versions.R")
assert_versions(c("metadat", "metafor"))
# Corpus rule: PREREG_ADDENDUM_2.md (dataset list and column mappings fixed before results).
args <- commandArgs(trailingOnly=TRUE)
destination <- if(length(args)) args[[1]] else "data/real-corpus.csv"
sources <- file.path(dirname(destination), "sources")
dir.create(sources, recursive=TRUE, showWarnings=FALSE)
options(digits=17)
rows <- list()
add <- function(id, dataset, row, measure, point, lo, hi, rare=FALSE) {
  stopifnot(all(is.finite(c(point, lo, hi))), lo <= point, point <= hi)
  rows[[length(rows)+1L]] <<- data.frame(id, dataset, row, measure, point, lo, hi, rare)
}
load_dataset <- function(name) {
  e <- new.env()
  utils::data(list=name, package="metadat", envir=e)
  x <- as.data.frame(e[[name]])
  write.csv(x, file.path(sources, paste0(name, ".csv")), row.names=FALSE)
  x
}
need <- function(x, name, cols)
  if(!all(cols %in% names(x))) stop(name, " lacks declared columns: ", paste(setdiff(cols, names(x)), collapse=","))
excluded <- character()
note <- function(name, form, n) excluded <<- c(excluded, sprintf("%s %s: %d non-estimable rows excluded", name, form, n))

# Binary: cells = c(a, b, c, d) or events/totals = c(x1, n1, x2, n2)
binary <- list(
  dat.gibson2002=c(type="cells", "ai","bi","ci","di"),
  dat.anand1999=c(type="totals", "ai","n1i","ci","n2i"),
  dat.egger2001=c(type="totals", "ai","n1i","ci","n2i"),
  dat.graves2010=c(type="totals", "ai","n1i","ci","n2i"),
  dat.hahn2001=c(type="totals", "ai","n1i","ci","n2i"),
  dat.hine1989=c(type="totals", "ai","n1i","ci","n2i"),
  dat.laopaiboon2015=c(type="totals", "ai","n1i","ci","n2i"),
  dat.lau1992=c(type="totals", "ai","n1i","ci","n2i"),
  dat.lee2004=c(type="totals", "ai","n1i","ci","n2i"),
  dat.li2007=c(type="totals", "ai","n1i","ci","n2i"),
  dat.linde2005=c(type="totals", "ai","n1i","ci","n2i"),
  dat.nielweise2007=c(type="totals", "ai","n1i","ci","n2i"),
  dat.yusuf1985=c(type="totals", "ai","n1i","ci","n2i"),
  dat.hart1999=c(type="totals", "x1i","n1i","x2i","n2i"),
  dat.bcg=c(type="cells", "tpos","tneg","cpos","cneg"),
  dat.colditz1994=c(type="cells", "tpos","tneg","cpos","cneg"),
  dat.damico2009=c(type="totals", "xt","nt","xc","nc"),
  dat.hartmannboyce2018=c(type="totals", "x.nrt","n.nrt","x.ctrl","n.ctrl"),
  dat.dorn2007=c(type="totals", "x.a","n.a","x.p","n.p"),
  dat.moore1998=c(type="totals", "Ee","Ne","Ec","Nc"),
  dat.viechtbauer2021=c(type="totals", "xTi","nTi","xCi","nCi"),
  dat.collins1985a=c(type="totals", "b.xti","nti","b.xci","nci"),
  dat.cannon2006=c(type="totals", "ep1t","nt","ep1c","nc"),
  dat.thompson1999=c(type="cells", "ihd.exp","noihd.exp","ihd.cont","noihd.cont"),
  dat.vanhowe1999=c(type="cells", "cir.pos","cir.neg","non.pos","non.neg"),
  dat.landenberger2005=c(type="cells", "n.cbt.rec","n.cbt.non","n.ctrl.rec","n.ctrl.non"))
for(name in names(binary)) {
  spec <- binary[[name]]; cols <- unname(spec[-1])
  x <- load_dataset(name); need(x, name, cols)
  v <- lapply(cols, function(k) as.numeric(x[[k]]))
  for(measure in c("RR","OR")) {
    e <- if(spec[["type"]]=="cells")
      metafor::escalc(measure=measure, ai=v[[1]], bi=v[[2]], ci=v[[3]], di=v[[4]], add=0.5, to="only0")
    else
      metafor::escalc(measure=measure, ai=v[[1]], n1i=v[[2]], ci=v[[3]], n2i=v[[4]], add=0.5, to="only0")
    ok <- is.finite(e$yi) & is.finite(e$vi)
    note(name, measure, sum(!ok))
    for(i in which(ok)) {
      ci <- exp(e$yi[i] + c(-1,1)*qnorm(.975)*sqrt(e$vi[i]))
      for(rare in if(measure=="OR") c(FALSE,TRUE) else FALSE)
        add(sprintf("%s-%03d-%s-%s", sub("^dat\\.","",name), i, measure, rare),
            paste0("metadat::", name), i, measure, exp(e$yi[i]), ci[1], ci[2], rare)
    }
  }
}

continuous <- list(
  dat.curtis1998=c("m1i","sd1i","n1i","m2i","sd2i","n2i"),
  dat.normand1999=c("m1i","sd1i","n1i","m2i","sd2i","n2i"),
  dat.dagostino1998=c("mt","sdt","nt","mc","sdc","nc"),
  dat.furukawa2003=c("Me","Se","Ne","Mc","Sc","Nc"))
g <- load_dataset("dat.gibson2002")
if(all(continuous$dat.normand1999 %in% names(g))) continuous$dat.gibson2002 <- continuous$dat.normand1999
for(name in names(continuous)) {
  cols <- continuous[[name]]
  x <- load_dataset(name); need(x, name, cols)
  v <- lapply(cols, function(k) as.numeric(x[[k]]))
  e <- metafor::escalc(measure="SMD", m1i=v[[1]], sd1i=v[[2]], n1i=v[[3]],
                       m2i=v[[4]], sd2i=v[[5]], n2i=v[[6]], vtype="LS")
  ok <- is.finite(e$yi) & is.finite(e$vi)
  note(name, "SMD", sum(!ok))
  for(i in which(ok)) {
    ci <- e$yi[i] + c(-1,1)*qnorm(.975)*sqrt(e$vi[i])
    add(sprintf("%s-%03d-SMD", sub("^dat\\.","",name), i),
        paste0("metadat::", name), i, "SMD", e$yi[i], ci[1], ci[2])
  }
}
out <- do.call(rbind, rows)
stopifnot(!anyDuplicated(out$id))
dir.create(dirname(destination), recursive=TRUE, showWarnings=FALSE)
write.csv(out, destination, row.names=FALSE, na="")
cat(excluded, sep="\n")
cat(nrow(out), "real-data configurations from", length(unique(out$dataset)),
    "datasets generated; these are inputs, not EValue validation results\n")
