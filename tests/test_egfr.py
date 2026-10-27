"""What "done" means for egfr.py. It is done when these pass:  uv run pytest

egfr.py should provide:
  ckd_epi_2021(scr, age, sex)   eGFR in mL/min/1.73 m2; scr in mg/dL, age in years, sex "F" or "M"
  to_mg_dl(value, unit)         creatinine in mg/dL from "mg/dL" or "umol/L"
  parse_date(text, site)        a datetime.date from a collection date as that site writes it
  rapid_decliners(results)      (set of patient IDs, number of assessable patients), from a table with
                                columns patient_id, date, egfr
"""
import datetime as dt

import pandas as pd
import pytest

from egfr import ckd_epi_2021, parse_date, rapid_decliners, to_mg_dl


# CKD-EPI 2021, no race term (Inker et al., N Engl J Med 2021;385:1737-49)
@pytest.mark.parametrize('scr, age, sex, expected', [
    (1.0, 50, 'F', 68.63),
    (1.2, 60, 'M', 69.23),
    (0.6, 30, 'F', 123.76),   # below kappa: the other exponent applies
    (2.0, 75, 'M', 34.16),
    (0.8, 45, 'M', 111.22),
])
def test_ckd_epi_2021(scr, age, sex, expected):
    assert ckd_epi_2021(scr, age, sex) == pytest.approx(expected, abs=0.05)


def test_units():
    assert to_mg_dl(88.4, 'umol/L') == pytest.approx(1.0)
    assert to_mg_dl(1.25, 'mg/dL') == pytest.approx(1.25)
    with pytest.raises(ValueError):
        to_mg_dl(1.0, 'mmol/L')


def test_dates():
    assert parse_date('2025-04-03', 'A') == dt.date(2025, 4, 3)
    assert parse_date('03/04/2025', 'B') == dt.date(2025, 4, 3)   # site B writes the day first
    assert parse_date('25/12/2024', 'B') == dt.date(2024, 12, 25)
    assert parse_date('2024-12-25', 'C') == dt.date(2024, 12, 25)


def test_rapid_decliners():
    results = pd.DataFrame([
        ('fast', '2024-01-10', 60), ('fast', '2024-07-28', 40),        # down 33% in 200 days: rapid
        ('mild', '2024-01-10', 60), ('mild', '2024-07-28', 45),        # down 25%: not rapid
        ('slow', '2024-01-10', 60), ('slow', '2025-02-13', 40),        # down 33%, but over 400 days: not rapid
        ('rise', '2024-01-10', 40), ('rise', '2024-07-28', 60),        # going up is not a decline
        ('later', '2023-02-01', 70), ('later', '2024-03-01', 62),
        ('later', '2024-09-01', 41),                                   # down 34% from 62 within 184 days: rapid
        ('once', '2024-05-05', 30),                                    # one result: not assessable
        ('twice', '2024-05-05', 30), ('twice', '2024-05-05', 30),      # one result sent twice: still one date
    ], columns=['patient_id', 'date', 'egfr'])
    results['date'] = pd.to_datetime(results.date)
    decliners, assessable = rapid_decliners(results)
    assert decliners == {'fast', 'later'}
    assert assessable == 5
