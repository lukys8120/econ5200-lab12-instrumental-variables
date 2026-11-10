"""Instrumental-variables helpers that never report a second stage alone (ECON 5200 Lab 12).

The design rule: every 2SLS estimate comes back with its first-stage F beside it,
because an IV estimate read without its first stage cannot be interpreted.
"""
import pandas as pd
import statsmodels.api as sm
from linearmodels.iv import IV2SLS


def first_stage(df: pd.DataFrame, endog: str, instruments: list[str],
                controls: list[str] | None = None) -> dict:
    """The first-stage coefficients on the instruments, their joint F, and n."""
    controls = controls or []
    fit = sm.OLS(df[endog], sm.add_constant(df[instruments + controls])).fit()
    hypotheses = [f"{z} = 0" for z in instruments]    # every instrument's coefficient is zero
    test = fit.f_test(hypotheses)
    return {"coef": fit.params[instruments], "F": float(test.fvalue), "n": int(fit.nobs)}


def iv_estimate(df: pd.DataFrame, outcome: str, endog: str, instruments: list[str],
                controls: list[str] | None = None) -> pd.Series:
    """2SLS, with robust standard errors, and the first-stage F attached."""
    controls = controls or []
    fit = IV2SLS(df[outcome], sm.add_constant(df[controls]), df[endog], df[instruments]).fit()
    return pd.Series({"estimate": fit.params[endog],
                      "std_err": fit.std_errors[endog],
                      "first_stage_F": first_stage(df, endog, instruments, controls)["F"],
                      "n": fit.nobs})


def exclusion_sensitivity(df: pd.DataFrame, outcome: str, endog: str, instrument: str,
                          gammas, controls: list[str] | None = None) -> pd.DataFrame:
    """The 2SLS estimate if the instrument had a direct effect gamma on the outcome.

    Subtracting gamma * instrument from the outcome removes that direct path: Conley,
    Hansen and Rossi's (2012) "plausibly exogenous" idea, one gamma at a time.
    """
    rows = []
    for gamma in gammas:
        adjusted = df.copy()
        adjusted[outcome] = df[outcome] - gamma * df[instrument]
        estimate = iv_estimate(adjusted, outcome, endog, [instrument], controls)["estimate"]
        rows.append({"gamma": gamma, "estimate": estimate})
    return pd.DataFrame(rows)
