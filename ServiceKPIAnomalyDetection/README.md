# 📈 Service KPI Anomaly Detection

This project tackles **anomaly (outlier) detection** in service Key Performance Indicators (KPIs) using real organizational data. The aim is to identify unusual patterns in KPIs for hundreds of services, helping to flag potential issues and understand service behavior.

---

## 🗂️ Dataset Overview

- **Time Period:** 45 days
- **Services:** 776
- **KPIs:** 7 (not all services have all KPIs measured)
- **Rows:** 94746 (with missing values before cleaning)

**Columns:**
1. `FullDate` – Date of KPI measurement
2. `ServiceID` – ID of the service
3. `KPI_ID` – ID indicating which KPI is measured
4. `Value` – Value of the KPI (numerical or percent as string)

---

## 🧹 Data Preprocessing

Two main data issues were identified:
1. **Missing ServiceID:** More than 31,075 missing values in the `ServiceID` column.
2. **Value Format:** Percentages in `Value` stored as strings (e.g., "97.2%") instead of float.

**Solutions:**
- Removed all samples with missing values in `ServiceID`.
- Cleaned the `Value` column:
  - Removed `%` sign
  - Converted to `float`
  - Divided by 100 if percentage
- Added derived features:
  - `Day` (e.g., Monday, Tuesday, ...)
  - `Week` (Week 1, Week 2, ...), for time-aware analysis

---

## 🔎 Data Exploration

- Plotted graphs to visualize KPIs across services and time.
- Explored patterns by **service**, **KPI**, **day of week**, and **week number**.

---

## 📊 Grouping Strategies

For robust anomaly detection, data was grouped in three ways:
1. By `ServiceID` and `KPI_ID`
2. By `ServiceID`, `KPI_ID`, and day of week (`Day`)
3. By `ServiceID`, `KPI_ID`, and week number (`Week`)

---

## 🚦 Anomaly Detection Methods

Outlier detection was performed on each group using three different methods:

### 1. Statistical: IQR Method
- Using the famous Q1-1.5×IQR / Q3+1.5×IQR formula.
- **Pros:** Simple, fast, intuitive.
- **Cons:** Can be too strict—if Q1=Q3, *any* different value is an outlier.

### 2. Machine Learning: COPOD Model
- COPOD is a robust unsupervised outlier detector.
- **Pros:** No hyperparameter tuning or feature scaling required, easy to use, works well on this type of data.
- **Cons:** Not suitable for high-dimensional data

### 3. Machine Learning: Isolation Forest
- Suitable for high-dimensional data.
- **Pros:** Widely used for anomaly detection.
- **Cons:** Needs feature scaling and hyperparameter tuning, more complex to use.

---

## 💡 Observations

- The IQR method is very strict and can flag small deviations as anomalies.
- COPOD performed better overall with less strict assumptions.
- Isolation Forest is powerful for more complex, high-dimensional cases, but requires careful configuration.

---

## 🚀 Usage

1. **Data Cleaning:**  
   Removed missing `ServiceID` and cleans `Value` format.
2. **Feature Engineering:**  
   Day of week and week number columns added.
3. **Grouping:**  
   Data is grouped for anomaly detection as described above.
4. **Anomaly Detection:**  
   Choose your method: IQR, COPOD, or Isolation Forest.

---

## 📈 Results

- **Statistical Method (IQR):** Most strict, may overflag.
- **COPOD:** Best balance of ease and effectiveness for this dataset.
- **Isolation Forest:** Useful if you extend to more features.

> **Overall:** Anomaly detection results can be visualized or exported for business analysis.

---

**Detect service anomalies—improve your operational insight!**
