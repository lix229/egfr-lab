---
name: egfr-qc
description: The lab's quality-control protocol for creatinine results from sites A, B and C, and the CKD-EPI 2021 formula. Load it before reading data/site_*.csv or computing eGFR.
---

# Creatinine QC protocol

Apply these steps to each site's file, in this order.

1. **Dates.** Sites A and C write ISO dates (2025-04-03). Site B writes the day first: 03/04/2025 is 3 April 2025.
   Parse each site with its own explicit format; never let a parser guess.
2. **Units.** Convert every value to mg/dL using that row's own unit: mg/dL as is, umol/L divided by 88.4.
   Site C mixes the two units, even within one patient.
3. **Repeats.** Site A's interface sometimes sends a result twice. Drop exact duplicate rows
   (same patient, date, value and unit).
4. **Plausibility.** Keep creatinine between 0.2 and 15 mg/dL. Report anything outside; don't silently drop it.
5. **Assessable patients.** A patient needs results on at least two different dates. Report how many are not
   assessable and leave them out of every denominator.

## eGFR, CKD-EPI 2021 (mL/min/1.73 m²)

    142 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^−1.200 × 0.9938^age × 1.012 (if female)

κ = 0.7 (female) or 0.9 (male); α = −0.241 (female) or −0.302 (male); Scr in mg/dL; age in years.
Source: Inker et al., N Engl J Med 2021;385:1737–49.

## Before you report
Say how many rows each site had, how many you dropped at each step and why, and how many patients were assessable.
