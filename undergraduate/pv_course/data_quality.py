"""Shared time-grid validation and interval-mean energy integration."""
import numpy as np
import pandas as pd


def validate_time_index(index, step_minutes=10):
    if not isinstance(index, pd.DatetimeIndex) or len(index) == 0:
        raise ValueError('A nonempty DatetimeIndex is required.')
    if step_minutes <= 0 or not np.isfinite(step_minutes):
        raise ValueError('step_minutes must be positive.')
    if index.hasnans or index.has_duplicates or not index.is_monotonic_increasing:
        raise ValueError('Timestamps must be unique, ordered and nonmissing.')
    step = pd.Timedelta(minutes=step_minutes)
    if len(index) > 1 and np.any(np.diff(index.asi8) % step.value != 0):
        raise ValueError('Irregular timestamps: differences must be multiples of the declared interval.')
    return step


def coverage_report(frame, step_minutes=10):
    """Report timestamp coverage separately from finite-value coverage; do not fill gaps."""
    step = validate_time_index(frame.index, step_minutes)
    idx = frame.index
    expected = int((idx[-1] - idx[0]) / step) + 1
    result = dict(start=str(idx[0]), end=str(idx[-1]), records=len(idx),
                  step_minutes=step_minutes, expected_intervals_within_span=expected,
                  missing_intervals_within_span=expected-len(idx),
                  timestamp_coverage_within_span=len(idx)/expected)
    if idx[0].year == idx[-1].year:
        start = pd.Timestamp(year=idx[0].year, month=1, day=1, tz=idx.tz)
        end = pd.Timestamp(year=idx[0].year+1, month=1, day=1, tz=idx.tz)
        annual = int((end-start)/step)
        result.update(calendar_year=idx[0].year, expected_calendar_intervals=annual,
                      missing_calendar_intervals=annual-len(idx), calendar_coverage=len(idx)/annual)
    numeric = frame.select_dtypes(include='number')
    result['invalid_values'] = {c:int((~np.isfinite(numeric[c])).sum()) for c in numeric}
    return result


def interval_energy(power, step_minutes=10):
    """W → Wh (or W/m² → Wh/m²), assuming each observation represents one interval mean.

    Missing intervals contribute no inferred energy. NaN values stay NaN; use
    sum(min_count=1) and report coverage. Never bridge a multi-hour/day gap.
    """
    validate_time_index(power.index, step_minutes)
    if np.isinf(power.to_numpy(dtype=float)).any():
        raise ValueError('Infinite power/irradiance is invalid.')
    if (power.dropna() < 0).any():
        raise ValueError('Negative power/irradiance is invalid.')
    return power * (step_minutes / 60)
