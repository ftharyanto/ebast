# Earthquake decay calculation logic (core calculation)
# This file is adapted from the provided earthquake_decay.py for Django integration.
# Place calculation functions here for import/use in Django views.

import numpy as np
from scipy.stats import linregress
import matplotlib.dates as mdates
import datetime as dt
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def regression(x, y):
    valid_indices = np.where((np.isfinite(x)) & (np.isfinite(y)))[0]
    if len(valid_indices) < 2:
        raise ValueError("Not enough valid data points for regression.")
    x_clean, y_clean = x[valid_indices], y[valid_indices]
    slope, intercept, r_value, _, _ = linregress(x_clean, y_clean)
    return r_value, slope, intercept

def bin_event_times(datetimes, interval=1.0, unit="Days"):
    """
    Bin event datetimes into intervals and return bin centers and frequencies.
    Args:
        datetimes (list of datetime.datetime): List of event datetimes.
        interval (float): Interval size.
        unit (str): 'Days' or 'Hours'.
    Returns:
        rentang_count: np.ndarray, time count axis (1, 2, ... intervals)
        frekuensi: np.ndarray, number of events per bin
        rentang_centers: np.ndarray, bin centers as matplotlib datenums
        jam2hari: float, conversion factor
    """
    datnum = mdates.date2num(datetimes)
    datnum.sort()
    if unit == "Hours":
        jam2hari = 1 / 24
        period_in_days = interval / 24
    else:
        jam2hari = 1
        period_in_days = interval
    start_time, end_time = datnum[0], datnum[-1]
    bins = np.arange(start_time, end_time + period_in_days, period_in_days)
    frekuensi, rentang_edges = np.histogram(datnum, bins=bins)
    rentang_centers = (rentang_edges[:-1] + rentang_edges[1:]) / 2
    rentang_count = np.arange(1, len(frekuensi) + 1) * interval
    return rentang_count, frekuensi, rentang_centers, jam2hari

def omori_model(rentang_count, frekuensi):
    """Omori model calculation."""
    y = 1 / frekuensi
    x = rentang_count
    r, B, A = regression(x, y)
    a = 1 / B
    b = A * a
    t1 = (a - b)
    tt = np.linspace(rentang_count[0], t1, 500)
    nt = a / (tt + b)
    return {
        "r": r, "a": a, "b": b, "t1": t1, "tt": tt, "nt": nt
    }

def mogi1_model(rentang_count, frekuensi):
    """Mogi I model calculation."""
    y = np.log10(frekuensi)
    x = np.log10(rentang_count)
    r, B, A = regression(x, y)
    a = 10 ** A
    b = -B
    t1 = 10 ** (np.log10(a) / b)
    tt = np.linspace(rentang_count[0], t1, 500)
    nt = a * tt ** (-b)
    return {
        "r": r, "a": a, "b": b, "t1": t1, "tt": tt, "nt": nt
    }

def mogi2_model(rentang_count, frekuensi):
    """Mogi II model calculation."""
    y = np.log(frekuensi)
    x = rentang_count
    r, B, A = regression(x, y)
    a = np.exp(A)
    b = -B
    t1 = np.log(a) / b
    tt = np.linspace(rentang_count[0], t1, 500)
    nt = a * np.exp(-b * tt)
    return {
        "r": r, "a": a, "b": b, "t1": t1, "tt": tt, "nt": nt
    }

def utsu_model(rentang_count, frekuensi):
    """Utsu model calculation."""
    c = 0.01
    y = np.log10(frekuensi)
    x = np.log10(rentang_count + c)
    r, B, A = regression(x, y)
    a = 10 ** A
    b = -B
    t1 = 10 ** (np.log10(a) / b) - c
    tt = np.linspace(rentang_count[0], t1, 500)
    nt = a * (tt + c) ** (-b)
    return {
        "r": r, "a": a, "b": b, "t1": t1, "tt": tt, "nt": nt
    }

def run_earthquake_decay_models(datetimes, interval=1.0, unit="Days", models=None):
    """
    Run selected earthquake decay models on event datetimes.
    Args:
        datetimes (list of datetime.datetime): Event times.
        interval (float): Bin interval.
        unit (str): 'Days' or 'Hours'.
        models (list): List of models to run ("omori", "mogi1", "mogi2", "utsu").
    Returns:
        dict: Results for each model, plus binning info.
    """
    if models is None:
        models = ["omori", "mogi1", "mogi2", "utsu"]
    rentang_count, frekuensi, rentang_centers, jam2hari = bin_event_times(datetimes, interval, unit)
    results = {"bin_centers": rentang_centers, "frequencies": frekuensi, "rentang_count": rentang_count}
    for model in models:
        try:
            if model == "omori":
                results["omori"] = omori_model(rentang_count, frekuensi)
            elif model == "mogi1":
                results["mogi1"] = mogi1_model(rentang_count, frekuensi)
            elif model == "mogi2":
                results["mogi2"] = mogi2_model(rentang_count, frekuensi)
            elif model == "utsu":
                results["utsu"] = utsu_model(rentang_count, frekuensi)
        except Exception as e:
            results[model] = {"error": str(e)}
    return results
