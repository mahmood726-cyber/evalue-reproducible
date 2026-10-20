source("analysis/versions.R")
assert_versions(character())
REQUIRED[["R"]] <- "0.0.0"
rejected <- tryCatch({assert_versions(character()); FALSE}, error=function(e) {
  cat(conditionMessage(e), "\n"); TRUE
})
if(!rejected) stop("Wrong-version mutation escaped")
cat("Wrong-version mutation rejected\n")
