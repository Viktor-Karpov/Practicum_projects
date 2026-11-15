# A/B Test Audit & Statistical Hypothesis Testing

Final project of the Yandex Practicum "Data Analyst" program (base course).
Two independent studies in one notebook.

## Part 1 — Hypothesis testing: Yandex Books

- **Question:** do users from Saint Petersburg spend more time reading and
  listening to books in the app than users from Moscow?
- Checked user IDs for duplicates, compared group sizes, statistics and
  distributions (histograms)
- One-sided Welch's t-test on user-level activity time (alpha = 0.05)
- **Result:** p-value = 0.3381 — no evidence that SPb users are more active;
  discussed possible causes (activity mode mix, outliers) and noted that the
  sample may lack power for a definitive answer

## Part 2 — A/B test audit: BitMotion Kit online store

- Audited the correctness of an A/B test of a new store interface:
  - removed users who participated in several tests or groups at once
  - checked group balance and intersections between groups
  - limited the analysis horizon to the first 7 days after registration
    (per the test specification)
  - estimated the required sample size with the Evan Miller calculator
- Metric: conversion to purchase (proportion) → two-proportion Z-test
- **Result:** conversion increased significantly in the test group —
  the new interface can be rolled out

## Data

Datasets are provided by Yandex Practicum as part of the course materials
and are not included in the repository. Part 2 datasets are loaded directly
from the public Yandex S3 URLs in the code, so those cells run as-is.

## Stack

Python, pandas, matplotlib, seaborn, scipy (Welch's t-test),
statsmodels (proportions_ztest)

## How to run

The notebook runs top-to-bottom in Jupyter or Google Colab.
