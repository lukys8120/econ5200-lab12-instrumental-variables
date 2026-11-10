# Instrumental Variables: Weak Instruments, Compliers and the Exclusion Restriction

**ECON 5200 · Causal Machine Learning & Applied Analytics · Lab 12**

## Objective

I diagnosed three ways an instrumental-variables estimate can mislead: an instrument too weak to trust, an estimate that belongs only to the people the instrument moved, and an instrument with a small direct effect on the outcome.

## Methodology

- Simulated samples where the true effect was 1.0 and an unobserved confounder biased OLS upward, then varied the instrument's first-stage strength from 0.01 to 1.0 and compared OLS and two-stage least squares (2SLS) over 500 draws at each strength.
- Replicated Card's (1995) estimate of the return to schooling, using growing up near a four-year college as the instrument, on 3,010 men from the National Longitudinal Survey.
- Added a direct path from the instrument to the outcome in the simulation and measured how far the 2SLS estimate moved as that path grew. Then ran the same sensitivity check on Card's data.
- Wrote my own 2SLS function from two OLS regressions and checked it against the `linearmodels` package.
- Used an `iv_tools.py` module that returns the first-stage F with every 2SLS estimate.

## Key Findings

**A weak instrument slides toward OLS.** With a strong first stage the median 2SLS estimate was 0.996, on the truth. At a median first-stage F of 0.5, the median 2SLS estimate was 2.038, against a median OLS estimate of 1.998.

**A significant 2SLS estimate from a weak instrument is usually wrong.** At a median F of 2.5, 31.4% of draws were significant at the 5% level, and 75.2% of those were more than 0.5 from the truth. At a median F of 0.5, 21.0% were significant and 98.1% of those were off by more than 0.5. Only the first-stage F warns you.

**Card's IV estimate is larger than OLS.** The first-stage F was 16.7, the OLS return to schooling 0.0740 and the 2SLS return 0.1323. This estimate applies to the men whose schooling depended on living near a college, not to everyone.

**A small exclusion violation can undo the result.** In the simulation, the bias from a direct effect is that effect divided by the first-stage strength, and a direct effect of 0.25 moved the estimate by more than half the true effect. In Card's data, a direct effect of just 0.02 log points pulls the 2SLS return down to 0.0730, about the OLS estimate.

**My own 2SLS function matches the package.** It reproduced 0.1323 with F = 16.7, and gave 0.2587 with F = 58.0 when the only controls were experience and its square.

## Repository Contents

| File | Description |
|---|---|
| `lab-ch12-diagnostic.ipynb` | Full lab notebook with rendered output |
| `src/iv_tools.py` | First-stage F, 2SLS with the first-stage F attached, and an exclusion-restriction sensitivity check |

## Data

- Card (1995) college-proximity data, loaded from the `wooldridge` package (`card`, 3,010 men).
- All other data are simulated with a fixed seed (`RANDOM_STATE = 42`).
