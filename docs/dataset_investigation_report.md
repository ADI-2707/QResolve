# Dataset Investigation Report

## Project

QResolve – AI-Powered Support Ticket Priority Prediction

---

## Objective

The objective of this investigation was to determine whether the original customer support ticket dataset is suitable for supervised machine learning.

The investigation focused on identifying data quality issues that could negatively affect the performance of ticket priority prediction models.

---

# Dataset

Original Dataset:

```
data/raw/customer_support_tickets.csv
```

Target Variable:

```
Ticket Priority
```

Classes:

- Low
- Medium
- High
- Critical

---

# Investigation Performed

The following analyses were conducted.

## 1. Duplicate Ticket Description Analysis

Identical ticket descriptions were grouped together.

The number of unique priority labels assigned to each description was calculated.

Result:

- 41 duplicate ticket descriptions were assigned multiple priority labels.

---

## 2. Keyword Analysis

Priority-related keywords were searched throughout the dataset.

Keywords included:

- urgent
- immediately
- emergency
- important
- critical
- as soon as possible

Result:

The same keywords appeared across multiple priority classes.

Example:

```
urgent

High
Low
Medium
Critical
```

This indicates that keywords alone do not determine the assigned priority.

---

## 3. Manual Inspection

Several duplicate ticket descriptions were manually inspected.

Observation:

The exact same ticket description appeared with different:

- Ticket Subject
- Ticket Priority

Example:

Same description

↓

Hardware Issue → Critical

Battery Issue → Low

Delivery Problem → Medium

Refund Request → Critical

This demonstrates that identical customer text maps to different target labels.

---

# Findings

The investigation identified several critical issues.

## Issue 1

Identical ticket descriptions are assigned different priority labels.

This violates the assumptions required for supervised learning.

---

## Issue 2

The same customer language appears across all priority classes.

Priority cannot be reliably inferred from the ticket text alone.

---

## Issue 3

Contradictory labels introduce noise into the training data.

Machine learning models cannot learn a deterministic mapping between input text and target labels.

---

# Impact on Model Performance

These data quality problems explain the poor performance observed during baseline model training.

Improving preprocessing, feature engineering, or trying more complex algorithms cannot resolve contradictory labels.

The limitation originates from the dataset itself rather than the machine learning models.

---

# Engineering Decision

The original dataset will not be used for the final Ticket Priority Prediction system.

Instead, the project will adopt a higher-quality dataset with:

- Consistent priority labels
- Realistic customer support language
- Deterministic mapping between ticket text and priority
- Better suitability for supervised NLP

The original investigation is preserved in this repository as documentation of the data validation process.

---

# Lessons Learned

This investigation highlights an important principle in applied machine learning:

Model performance depends on data quality more than model complexity.

Before investing time in algorithm optimization, the underlying dataset must be verified for consistency and suitability.

Careful dataset validation can prevent misleading conclusions and unnecessary experimentation.