# All R entry points source this file and assert their dependency subset.
REQUIRED <- c(R="4.6.0", EValue="4.1.4", metadat="1.6.0", metafor="5.2.1")
assert_versions <- function(packages=c("EValue", "metadat", "metafor")) {
  actual <- c(R=as.character(getRversion()),
              vapply(packages, function(p)
                tryCatch(as.character(packageVersion(p)), error=function(e) "MISSING"), ""))
  expected <- REQUIRED[names(actual)]
  if (!identical(actual, expected))
    stop("Version gate failed: expected ", paste(names(expected), expected, collapse="; "),
         "; actual ", paste(names(actual), actual, collapse="; "), call.=FALSE)
  invisible(actual)
}
