# Addendum before local replay — 2026-10-20

Inventory found R 4.6.0, metadat 1.6-0 and metafor 5.2-1. EValue is absent from both inspected R installations and the user library. The repository contains an inherited 13-case synthetic reference explicitly identifying EValue 4.1.4 source functions (not an installed namespace), R 4.6.0 and jsonlite 2.0.0.

Pin the fresh installed oracle to EValue 4.1.4 to permit comparison with that provenance. R normalizes packageVersion values to metadat 1.6.0 and metafor 5.2.1. JSON processing is performed by Python; jsonlite is not a dependency of this archive's R scripts.

Add an explicitly separate inherited-fixture replay of all 13 cases, with the same five output quantities, 1e-9 tolerance and mutation safeguards. This cannot satisfy fresh R validation. The corpus generator can run with its own exact R/metadat/metafor pins while the top-level full validator refuses missing EValue.

The metafor data adapter uses escalc add=0.5, to="only0" for binary data, and bias-corrected SMD estimates with the default vtype="LS" variance, with qnorm(.975) Wald limits. All rows are retained or generation fails. No result-dependent dataset selection is allowed.

The MD reference adapter is prepared but unexecuted. The host must inspect EValue 4.1.4 installed help/source, confirm the declared matrix layout and standardized MD conversion, and document any necessary adapter correction before generating reference results. Any change of estimand requires a further preregistration addendum.
