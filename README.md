# Fuel Station Sales Reconciliation & Anomaly Detection

## Project Overview

A Python-based audit analytics project that compares fuel station Point of Sale (POS) sales records against physical pump meter readings to identify discrepancies and potential operational losses.

## Business Problem

Fuel stations need reliable ways to monitor fuel dispensing and ensure that recorded sales match physical pump readings.

Discrepancies may arise from unrecorded dispensing, inaccurate sales records, equipment calibration issues, or potential fuel losses.

## Project Objectives

- Reconcile POS sales with physical meter readings.
- Calculate daily fuel dispensing volumes.
- Identify discrepancies in litres.
- Calculate variance percentages.
- Automatically flag unusual discrepancies.
- Generate an audit exception report.

## Technologies

- Python
- Pandas
- NumPy

## Methodology

1. Simulate POS sales and physical pump readings.
2. Calculate actual fuel dispensed.
3. Compare physical dispensing with recorded sales.
4. Calculate volume and percentage variances.
5. Apply a 0.5% anomaly threshold.
6. Generate an automated audit report.

## Key Findings

The simulated dataset covers two fuel pumps over ten days.

- Pump 2 recorded a 25-litre discrepancy on October 6, 2026.
- Pump 1 recorded a 5-litre discrepancy on October 10, 2026.

The system flags discrepancies exceeding the configured threshold.

## How to Run

Install dependencies:

```bash
pip install pandas numpy
```

Run the script:

```bash
python fuel_reconciliation.py
```

## Disclaimer

This project uses simulated data for demonstration purposes. Flagged discrepancies require further investigation and do not independently establish theft or fraud.

## Author

Chizimihe Modestus Agugo

GitHub: [chizimihe](https://github.com/chizimihe)
