"""Checks results/public.json, the answer to the extra question (public/QUESTION.md), against an answer computed from
the same NHANES files and, if it's off, says where to look.
usage: uv run checks/check_public.py"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
KEY = json.loads((HERE / 'public_answers.json').read_text())
FIELDS = ['below_60_2009', 'below_60_2021', 'black_below_60_2009', 'black_below_60_2021']
HINT = {'unweighted': 'These are shares of the sample. Weight each participant by the exam (MEC) weight, WTMEC2YR.',
        'age_18': 'This counts 18- and 19-year-olds too: QUESTION.md counts adults aged 20 or over.',
        'pregnant_kept': 'Leave out pregnant participants (RIDEXPRG is 1 for them).'}


def stop(*lines):
    print('NOT YET')
    for line in lines:
        print(' -', line)
    sys.exit(1)


def near(got, want):
    return all(abs(float(got[f]) - want[f]) <= .15 for f in FIELDS)


out = HERE.parent / 'results' / 'public.json'
if not out.exists():
    stop('Write results/public.json first (see public/QUESTION.md).')
try:
    got = json.loads(out.read_text())
    [float(got[f]) for f in FIELDS]
except (ValueError, KeyError, TypeError) as e:
    stop(f'Could not read results/public.json ({e!r}). It needs "adults" and {", ".join(FIELDS)}.')

want = KEY['answer']
if got.get('adults') == want['adults'] and near(got, want):
    print(f'PASS: {want["adults"]:,} adults. eGFR below 60: {want["below_60_2009"]}% with the 2009 equation, '
          f'{want["below_60_2021"]}% with 2021; among non-Hispanic Black adults, {want["black_below_60_2009"]}% '
          f'and {want["black_below_60_2021"]}%.')
    sys.exit(0)
for slip, numbers in KEY['slips'].items():   # a usual mistake gives these numbers exactly
    if got.get('adults') == numbers['adults'] and near(got, numbers):
        stop(HINT[slip])
problems = []
if got.get('adults') != want['adults']:
    problems.append(f'adults is {got.get("adults")}: count participants aged 20 or over, not pregnant, with a serum '
                    'creatinine result (and an exam weight).')
if not near(got, want):
    problems.append('The shares are off. Check the equations against QUESTION.md and the skill, that creatinine is in '
                    'mg/dL (LBXSCR, not LBDSCRSI), and that each share is weighted and in percent.')
stop(*problems)
