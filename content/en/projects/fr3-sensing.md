---
title: "FR3 Sensing"
description: "Machine learning-enabled multiband wireless sensing for activity recognition"
layout: "project-detail"
---

## Project Overview

This project develops a robust and privacy-preserving Human Activity Recognition (HAR) system using multi-band Channel State Information (CSI) from the FR3 spectrum. Whereas existing sensing systems rely on a single frequency band and exhibit strong susceptibility to environmental variation, this work exploits the complementary propagation characteristics of the bands between 7 GHz and 24 GHz to improve robustness and accuracy.

A Software-Defined Radio (SDR) platform based on USRP X310 units is used to collect synchronized CSI streams through time-division multiplexing, enabling dual-band fusion without hardware duplication. The system integrates a complete data collection pipeline, machine learning models for activity classification, and systematic evaluation across four progressively larger datasets.

### Datasets

We collected four datasets totaling over 80,000 labeled CSI samples. Each sample consists of complex-valued channel measurements across 250 subcarriers, 4 spatial streams, and 2 frequency bands.

| Dataset | Users | Activities | Description |
|---------|-------|------------|-------------|
| **Chair** | -- | 2 | Binary chair detection |
| **JTerm** | 1 | 10 | Single-user activity recognition |
| **Sunday** | 3 | 9 | Multi-user activity recognition |
| **Saturday** | 7 | 17 | Multi-user, 2 furniture orientations |

We train lightweight CNN classifiers (26K--1.2M parameters) as well as logistic regression baselines, evaluating across tasks including HAR, User Detection (UD), and joint User+Activity classification (UDHAR).

---

## Key Findings

**LOCO (Leave-One-Capture-Out):** Accuracy drops to ~57% when no recording session appears in both train and test sets.

**Controlled Leakage (Leak-1):** Adding just 1 sample per held-out capture recovers 94.3% -- the smoking gun proving models memorize per-capture CSI fingerprints, not activity patterns.

**Temporal Splits:** Training on earlier recordings and testing on later ones achieves 73--88%.

**LOUO (Leave-One-User-Out):** Accuracy drops to 18--36%, revealing user-specific RF signature memorization.

**Furniture orientation shift** drops accuracy to 14.6%, but mixing just 5% of target-orientation data recovers 78%, and 10% reaches 97%. Model size barely matters: milli_cnn (74K params) matches kilo_cnn (1.2M).

---

## Results

### Capture-Aware Splits

LOCO vs. Leak-1 evaluation showing how a single leaked sample per capture inflates accuracy from 57% to 94%.

![Capture-aware splits: LOCO vs Leak-1](/images/projects/capstone/loco_leak1.png)

### Random Split vs. Leave-One-User-Out

Comparison demonstrating that models memorize user-specific RF signatures rather than learning generalizable activity patterns.

![Random split vs LOUO](/images/projects/capstone/random_vs_louo.png)

### Orientation Gap Bridging

S-curve showing how increasing fractions of target-orientation data progressively bridge the orientation domain gap.

![Mix ratio sweep](/images/projects/capstone/mix_ratio_sweep.png)

### Saturday Evaluation Strategies

All Saturday dataset evaluation strategies compared side by side.

![Saturday comparison](/images/projects/capstone/saturday_comparison.png)

### Orientation Split Confusion Matrix

17-class confusion matrix under orientation shift -- near-uniform predictions indicate the model is effectively guessing.

![Orientation confusion matrix](/images/projects/capstone/orient_confusion.png)

### Model Size vs. Mix Ratio

Demonstrates that milli_cnn (74K params) matches kilo_cnn (1.2M params) across all target data fractions.

![Model size comparison](/images/projects/capstone/model_size_comparison.png)

### Temporal Splits

Sunday temporal split results across HAR, UD, and UDHAR tasks.

![Temporal splits](/images/projects/capstone/temporal_splits.png)

---

**Supervised by:** Prof. Marwa Chafii and Dr. Roberto Bomfin

**Tech:** Python, MATLAB
