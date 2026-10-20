# References for paper 22 (verified against Crossref, accessed 2026-10-20)

Vancouver style (BMC). Journal abbreviations = NLM. Titles are as deposited in Crossref (only HTML markup stripped). See references.json for raw fields and DOI resolution.

1. VanderWeele TJ, Ding P. Sensitivity Analysis in Observational Research: Introducing the E-Value. Ann Intern Med. 2017;167(4):268-74. doi:10.7326/m16-2607

2. Mathur MB, Ding P, Riddell CA, VanderWeele TJ. Web Site and R Package for Computing E-values. Epidemiology. 2018;29(5):e45-e47. doi:10.1097/ede.0000000000000864

3. Viechtbauer W. Conducting Meta-Analyses in R with the metafor Package. J Stat Softw. 2010;36(3):1-48. doi:10.18637/jss.v036.i03

4. Ali SM, Ahmad M, Khan L, Kiel J, O'Connor N, Kukreja N, et al. RapidMeta Cardiology: A Browser-Based Living Meta-Analysis Platform Validated Against Finerenone Phase III Trial Data [version 1; peer review: awaiting peer review]. F1000Res. 2026;15:838. doi:10.12688/f1000research.181441.1

5. VanderWeele TJ. Optimal approximate conversions of odds ratios and hazard ratios to risk ratios. Biometrics. 2020;76(3):746-52. doi:10.1111/biom.13197

6. Chinn S. A simple method for converting an odds ratio to effect size for use in meta-analysis. Stat Med. 2000;19(22):3127-31. doi:10.1002/1097-0258(20001130)19:22<3127::AID-SIM784>3.0.CO;2-M

7. Linden A, Mathur MB, VanderWeele TJ. Conducting sensitivity analysis for unmeasured confounding in observational studies using E-values: The evalue package. Stata J. 2020;20(1):162-75. doi:10.1177/1536867x20909696

8. VanderWeele TJ, Ding P, Mathur M. Technical Considerations in the Use of the E-Value. J Causal Inference. 2019;7(2):20180007. doi:10.1515/jci-2018-0007

## Software / web references (CRAN, accessed 20 Oct 2026)

9. Mathur MB, Smith LH, Ding P, VanderWeele TJ. EValue: Sensitivity Analyses for Unmeasured Confounding and Other Biases in Observational Studies and Meta-Analyses. R package version 4.1.4. 2025. https://cran.r-project.org/package=EValue. Accessed 20 Oct 2026.
10. Viechtbauer W, White T, Noble D, Senior A, Hamilton WK. metadat: Meta-Analysis Datasets. R package version 1.6-0. 2026. https://cran.r-project.org/package=metadat. Accessed 20 Oct 2026.  [authors = DESCRIPTION [aut] roles; Schwarzer G and Roever C are data contributors (dtc)]
11. Viechtbauer W. metafor: Meta-Analysis Package for R. R package version 5.2-1. 2026. https://cran.r-project.org/package=metafor. Accessed 20 Oct 2026.

## Verification notes

- [1] doi.org -> https://www.acpjournals.org/doi/10.7326/M16-2607 (doi.org 302; final landing HTTP 403; 403 = publisher bot-blocking of curl, DOI itself resolves). Crossref HTTP 200; 2 authors.
- [2] doi.org -> https://journals.lww.com/00001648-201809000-00026 (doi.org 302; final landing HTTP 403; 403 = publisher bot-blocking of curl, DOI itself resolves). Crossref HTTP 200; 4 authors.
- [3] doi.org -> https://www.jstatsoft.org/article/view/v036i03 (doi.org 302; final landing HTTP 200). Crossref HTTP 200; 1 authors.
- [4] doi.org -> https://f1000research.com/articles/15-838/v1 (doi.org 302; final landing HTTP 200). Crossref HTTP 200; 12 authors.
- [5] doi.org -> https://academic.oup.com/biometrics/article/76/3/746-752/7429123 (doi.org 302; final landing HTTP 403; 403 = publisher bot-blocking of curl, DOI itself resolves). Crossref HTTP 200; 1 authors.
- [6] doi.org -> https://onlinelibrary.wiley.com/doi/10.1002/1097-0258(20001130)19:22%3C3127::AID-SIM784%3E3.0.CO;2-M (doi.org 302; final landing HTTP 403; 403 = publisher bot-blocking of curl, DOI itself resolves). Crossref HTTP 200; 1 authors.
- [7] doi.org -> https://journals.sagepub.com/doi/10.1177/1536867X20909696 (doi.org 302; final landing HTTP 403; 403 = publisher bot-blocking of curl, DOI itself resolves). Crossref HTTP 200; 3 authors.
- [8] doi.org -> https://www.degruyterbrill.com/document/doi/10.1515/jci-2018-0007/html (doi.org 302; final landing HTTP 202; 202 = De Gruyter bot-challenge page, DOI itself resolves). Crossref HTTP 200; 3 authors.
- [3] Crossref title contains markup `<i>R</i>`/`<b>metafor</b>`; rendered as 'Conducting Meta-Analyses in R with the metafor Package'. Crossref gives no pages; jstatsoft.org meta tags give 1-48. Crossref issued year 2010.
- [4] EXISTS. F1000Research 2026;15:838, version 1 first published 01 Jun 2026; landing page states 'peer review: awaiting peer review' (as of 2026-10-20). 12 authors: Ali SM, Ahmad M, Khan L, Kiel J, O'Connor N, Kukreja N, Woo A, Quadri SF, Ahmad RR, Ahmad MT, Dar B, Ahmad T. F1000 requires the bracketed peer-review status in citations.
- [6] Old Wiley SICI-style DOI; Crossref stores it lower-case (10.1002/1097-0258(20001130)19:22<3127::aid-sim784>3.0.co;2-m). DOIs are case-insensitive; upper-case form shown is the publisher's.
- [7] Crossref container title is 'The Stata Journal: Promoting communications on statistics and Stata'; NLM-style abbreviation 'Stata J'.
- [8] Crossref lists third author as 'Mathur M' (given name 'Maya'); she usually publishes as Mathur MB. Article number 20180007 in J Causal Inference 7(2).
- [2] Authors per Crossref: Mathur MB, Ding P, Riddell CA, VanderWeele TJ. Epidemiology 2018;29(5):e45-e47.
- [5] Biometrics 2020;76(3):746-752; doi.org now redirects to academic.oup.com (Biometrics moved to OUP).
