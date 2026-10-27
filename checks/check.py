"""Checks results/ against the planted answer and, if it's off, says where to look.
usage: uv run checks/check.py

It reads results/summary.json ({"assessable_patients": n, "rapid_decliners": n}) and results/decliners.csv (a
patient_id column). The answer key next to this file is hashed: reading it won't help, solving the task will."""
import csv
import hashlib
import json
import pathlib
import sys
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE.parent
KEY = json.loads((HERE / 'answers.json').read_text())
HINT = {'A': 'site A sends some results twice', 'B': 'site B writes dates day-first',
        'C': 'site C mixes umol/L with mg/dL, even for one patient'}


def hashed(p):
    return hashlib.sha256((KEY['salt'] + p).encode()).hexdigest()[:12]


def sites(counts):
    return ', '.join(f'{n} at site {s}' for s, n in sorted(counts.items()))


def hints(counts):
    return '; '.join(HINT[s] for s in sorted(counts) if s in HINT)


def stop(*lines):
    print('NOT YET')
    for line in lines:
        print(' -', line)
    sys.exit(1)


summary_file, ids_file = LAB / 'results' / 'summary.json', LAB / 'results' / 'decliners.csv'
if not (summary_file.exists() and ids_file.exists()):
    stop('Write results/summary.json and results/decliners.csv first (see AGENTS.md).')
try:
    summary = json.loads(summary_file.read_text())
    with open(ids_file, newline='') as f:
        ids = {row['patient_id'].strip() for row in csv.DictReader(f)}
except (ValueError, KeyError) as e:
    stop(f'Could not read the results ({e}). summary.json must be JSON; decliners.csv needs a patient_id column.')
site = {row['patient_id']: row['site'] for row in csv.DictReader(open(LAB / 'data' / 'patients.csv', newline=''))}

problems = []
n = summary.get('assessable_patients')
if n != KEY['assessable']:
    if n == KEY['patients']:
        problems.append(f'assessable_patients is {n:,}: that counts everyone, including the {KEY["single_result"]} '
                        'patients with a single result.')
    elif n == KEY['assessable_if_duplicates_kept']:
        problems.append(f'assessable_patients is {n:,}: some single-result patients had that result sent twice. '
                        'Count dates, not rows.')
    else:
        problems.append(f'assessable_patients is {n}: not what the egfr-qc protocol gives.')
if summary.get('rapid_decliners') != len(ids):
    problems.append(f'summary.json says {summary.get("rapid_decliners")} rapid decliners, but decliners.csv lists {len(ids)}.')

truth, slow = KEY['decliners'], KEY['slow']
hits = {p for p in ids if hashed(p) in truth}
extra = ids - hits
slow_extra = {p for p in extra if hashed(p) in slow}
other_extra = Counter(site.get(p, '?') for p in extra - slow_extra)
missed = Counter(s for h, s in truth.items() if h not in {hashed(p) for p in hits})
if slow_extra:
    problems.append(f'{len(slow_extra)} of your decliners fell more than 30% only across more than 365 days. '
                    'Compare results no more than 365 days apart.')
if other_extra:
    problems.append(f'{sum(other_extra.values())} of your decliners are not rapid decliners ({sites(other_extra)}). '
                    f'Check: {hints(other_extra)}.')
if missed:
    problems.append(f'You missed {sum(missed.values())} rapid decliners ({sites(missed)}). Check: {hints(missed)}.')
if problems:
    stop(*problems)
print(f'PASS: {len(ids)} rapid decliners among {n:,} assessable patients ({100 * len(ids) / n:.1f}%).')
