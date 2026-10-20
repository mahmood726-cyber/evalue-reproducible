# Fresh installed-package oracle. Must not reuse repository fixture values.
source("analysis/versions.R")
assert_versions()
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==2L)
d <- read.csv(args[[1]], stringsAsFactors=FALSE, na.strings="")
stopifnot(nrow(d)>0L, !anyDuplicated(d$id))
options(digits=17)
api <- c("evalues.RR","evalues.OR","evalues.HR","evalues.MD","evalues.OLS",
         "evalues.RD","confounded_meta","sens_plot")
stopifnot(all(api %in% getNamespaceExports("EValue")))
matrix_result <- function(x) {
  if(!is.matrix(x) || !identical(dim(x), c(2L,3L)))
    stop("Unexpected EValue result shape: inspect pinned package API before changing adapter")
  x
}
result <- lapply(seq_len(nrow(d)), function(i) {
  x <- d[i,]
  if(x$measure=="SMD") {
    # Pointwise MD adapter: standardized differences, not the package's se-based CI.
    at <- function(v) matrix_result(EValue::evalues.MD(est=v, sd=1))
    r <- at(x$point)
    rp <- r[1,1]; ep <- r[2,1]
    rl <- rh <- ec <- NA_real_
    if(!is.na(x$lo)) {
      a <- at(x$lo); b <- at(x$hi)
      rl <- a[1,1]; rh <- b[1,1]
      ec <- if(x$lo<=0 && x$hi>=0) EValue::evalues.RR(1)[2,1] else
        if(x$point>=0) a[2,1] else b[2,1]
    }
  } else {
    f <- getExportedValue("EValue", paste0("evalues.", x$measure))
    a <- list(est=x$point, lo=x$lo, hi=x$hi)
    if(x$measure!="RR") a$rare <- x$rare
    r <- matrix_result(suppressMessages(do.call(f,a)))
    rp <- r[1,1]; rl <- r[1,2]; rh <- r[1,3]; ep <- r[2,1]
    ec <- if(is.na(x$lo)) NA_real_ else min(r[2,2:3], na.rm=TRUE)
  }
  stopifnot(is.finite(ep), is.finite(rp))
  if(!is.na(x$lo)) stopifnot(all(is.finite(c(ec,rl,rh))))
  data.frame(id=x$id, point=ep, ci=ec, rr_point=rp, rr_lo=rl, rr_hi=rh)
})
write.csv(do.call(rbind,result), args[[2]], row.names=FALSE, na="")
writeLines(c(capture.output(sessionInfo()), paste("API exported:", paste(api, collapse=", "))),
           paste0(args[[2]], ".session.txt"))
cat(length(result), "fresh installed EValue configurations generated\n")
