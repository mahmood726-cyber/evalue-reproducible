# Run from archive root: Rscript --vanilla validate.R < NUL
source("analysis/versions.R")
assert_versions()
cat("Exact R/package versions PASS\n")
python <- Sys.getenv("PYTHON", unset="python")
status <- system2(python, c("-B","analysis/pipeline.py","full"), stdin="")
if(status != 0L) stop("Validation failed, exit ", status)
