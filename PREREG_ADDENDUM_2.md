# Addendum 2 before fresh EValue results — 2026-10-20 (host session, network available)

Written after installing the oracle and reading its source, and BEFORE any EValue output was generated for a corpus configuration. The only EValue calls made beforehand were API inspections (printed function bodies plus four hand-typed values: MD 0.5 with/without se, RR 1 [0.667,1.5], RR 2 [2,2], HR 1.6 common). None of them was a comparison with the app.

## Oracle installation

EValue 4.1.4 is the CRAN Windows binary (Packaged 2025-08-28; built under R 4.6.1), the same binary already installed for paper 20. It is copied into the lane-local library `<WORKSPACE>\r-library` (with MetaUtility 2.1.2 and jsonlite 2.0.0) and selected through `R_LIBS_USER`. `versions.R` asserts EValue 4.1.4 exactly, with R 4.6.0, metadat 1.6.0 and metafor 5.2.1. R warns that the binary was built under R 4.6.1. This warning is recorded and is not a failure.

## Adapter correction (non-substantive)

`EValue::evalues.MD` has the signature `(est, se = NA, true = 0, ...)`. There is no `sd` argument, so the prepared `sd=1` was silently absorbed by `...`. It is removed. `est` is already interpreted as a standardized difference d, and the function returns `evalues.RR(exp(0.91 d))`. The 2×3 matrix layout (rows RR / E-values; columns point / lower / upper) is confirmed.

The SMD CI convention is unchanged: each user-supplied SMD limit is transformed pointwise with `evalues.MD(limit)`, and the CI E-value comes from the limit nearest the null (1 if the interval contains 0). EValue's own se-based interval uses exp(0.91 d ± 1.78 se). The app's pointwise transform of d ± 1.96 se equals exp(0.91 d ± 1.7836 se). This convention difference is reported descriptively (`smd-se-convention.json`, the maximum relative difference of the RR limits) and is NOT counted as a pass or a failure.

## Expanded real-data corpus (replaces the 2-dataset real corpus; locked before results)

All rows of every metadat 1.6.0 dataset listed below are used. The mappings are fixed in advance; the arm order does not matter for this numerical comparison.

Binary (escalc RR and OR, add=0.5, to="only0"; RR run with rare=FALSE; OR with rare=FALSE and TRUE):
- `ai,bi,ci,di`: dat.gibson2002
- `ai,n1i,ci,n2i`: dat.anand1999, dat.egger2001, dat.graves2010, dat.hahn2001, dat.hine1989, dat.laopaiboon2015, dat.lau1992, dat.lee2004, dat.li2007, dat.linde2005, dat.nielweise2007, dat.yusuf1985
- `x1i,n1i,x2i,n2i`: dat.hart1999
- `tpos,tneg,cpos,cneg`: dat.bcg, dat.colditz1994
- events/totals: dat.damico2009 (xt,nt,xc,nc), dat.hartmannboyce2018 (x.nrt,n.nrt,x.ctrl,n.ctrl), dat.dorn2007 (x.a,n.a,x.p,n.p), dat.moore1998 (Ee,Ne,Ec,Nc), dat.viechtbauer2021 (xTi,nTi,xCi,nCi), dat.collins1985a (b.xti,nti,b.xci,nci), dat.cannon2006 (ep1t,nt,ep1c,nc)
- 2×2 cells: dat.thompson1999 (ihd.exp,noihd.exp,ihd.cont,noihd.cont), dat.vanhowe1999 (cir.pos,cir.neg,non.pos,non.neg), dat.landenberger2005 (n.cbt.rec,n.cbt.non,n.ctrl.rec,n.ctrl.non)

Continuous (escalc SMD, vtype="LS", Wald 95% limits):
- `m1i,sd1i,n1i,m2i,sd2i,n2i`: dat.curtis1998, dat.normand1999, and dat.gibson2002 if it has these columns
- dat.dagostino1998 (mt,sdt,nt,mc,sdc,nc); dat.furukawa2003 (Me,Se,Ne,Mc,Sc,Nc)

If a row has missing raw data, escalc returns a non-finite estimate. That row is excluded by this rule alone, and the number of exclusions per dataset is written to the generation log. No row is excluded for any other reason. If a listed dataset lacks a declared column, generation fails rather than skipping it.

Dataset CSVs are exported to `data/sources/`.

## Dense synthetic grid (added)

These are added to the original grid and edge cases, which are retained. Ratio measures (RR; OR and HR with rare FALSE/TRUE) use 101 log-spaced points from 0.02 to 50. SMD uses 121 points from −3 to 3. Each point is run with the CI [p/1.5, p·1.5] (SMD: [p−0.25, p+0.25]) and without a CI. These are purely numerical; HR is validated only on synthetic inputs because metadat has no raw HR data.

## Unchanged

Quantities, the 1e-9 tolerance relative to max(1,|R|), refusal probes, safeguards, fixed denominators and the scope gap (no OLS/RD/confounded_meta/sens_plot in the app) are unchanged. Planted defects are as in PREREG, and one more is added: a mutated copy of the app's `shared/evalue.js` (HR conversion constant 0.5 → 0.5000001) must fail when replayed through the page.
