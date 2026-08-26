# CSE437 Data Science: Project Report

## Cover
- **Project title:** Predicting PM2.5 Surges During Winter Inversions
- **Course, section, semester:** CSE437
- **Group members:** (Your Name & ID), (Mate's Name & ID)
- **GitHub repository link:** https://github.com/your-username/cse437-pm25-forecasting-6
- **Date:** 3 September 2026

## Summary
*(Write this last after both you and your mate have run all notebooks. 150-200 words covering dataset, problem, targets, models, metric, and finding.)*

---

## 1. Problem and Dataset (User - 65%)

### 1.1 Problem statement
High concentrations of PM2.5 present severe health hazards. Predicting sudden accumulation (surges) versus dispersion allows for better public health warnings.

### 1.2 Dataset
The dataset is the "Beijing Multi-Site Air-Quality Data Set" from the UCI Repository (https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data). It contains hourly observations. We filtered it down to 3 sites (Aotizhongxin, Changping, Dingling).

### 1.3 Target variable
PM2.5 (continuous numerical, $\mu\text{g}/\text{m}^3$). It is highly skewed right, with a long tail of extreme pollution events.

### 1.4 Three questions
1. How do orthogonal wind vector components ($u$ and $v$) and barometric pressure interact to drive local particulate accumulation versus atmospheric dispersion?
2. Can feature selection and dimensionality reduction (PCA) resolve severe multicollinearity among co-pollutants ($SO_2, NO_2, CO, O_3$) without degrading the model's predictive power during sudden pollution surges?
3. Under what seasonal meteorological conditions (such as winter thermal inversions) does the regression model exhibit its highest residual prediction errors, and why?

---

## 2. Data Handling and Preprocessing (User - 65%)

### 2.1 Data quality audit
*(Mate finds this out in Notebook 01)*

### 2.2 Missing values
We assumed missing values were due to sensor downtime. We used linear interpolation (up to 3 hours) for small gaps, and forward filling for larger gaps to preserve temporal continuity without leaking future data.

### 2.3 Outliers
*(Document what you found in Notebook 01)*

### 2.4 Transformation and scaling
Scaled using StandardScaler during the PCA pipeline.

### 2.5 Before and after
*(Add table comparing row counts before and after dropping NaNs created by lagging)*

---

## 3. Statistical Analysis (Mate - 35%)

### 3.1 Descriptive statistics
*(Fill from Notebook 01)*

### 3.2 Relationships
*(Insert correlation heatmap from Notebook 01)*

### 3.3 What the data says so far
*(Bullet points from EDA)*

---

## 4. Feature Engineering (Mate - 35%)

### 4.1 Derived features
Created lag features ($t-1, t-3, t-24$) and 24-hour rolling means to capture temporal dependence without data leakage. Calculated orthogonal wind vectors $u$ and $v$ from speed and direction. Cyclically encoded hour and month using sine/cosine.

### 4.2 Dimensionality reduction
Applied PCA (2 components) to the lagged co-pollutants ($PM10, SO_2, NO_2, CO, O_3$) to remove multicollinearity.

### 4.3 Feature selection
Dropped highly collinear original temporal and spatial features.

### 4.4 Final feature set
*(List final features)*

---

## 5. Modeling and Validation (User - 65%)

### 5.1 Validation strategy
Strict chronological split (Train: 2013-2015, Val: 2016, Test: 2017). Random split was avoided to prevent future data leakage. Used `TimeSeriesSplit` for CV.

### 5.2 Baseline
Ridge Regression ($\alpha=1.0$).

### 5.3 Model families
1. Ridge Regression (Linear): Assumes linear relationships, robust to collinearity (though we mitigated this via PCA).
2. XGBoost (Tree-based ensemble): Handles non-linear interactions well, specifically the interaction between temperature and pressure.

### 5.4 Metrics
Primary metric: Root Mean Squared Error (RMSE) to heavily penalize large prediction errors during pollution surges. Secondary: MAE.

---

## 6. Hyperparameter Tuning (User - 65%)

### 6.1 Search space
- `n_estimators`: [50, 100, 200]
- `max_depth`: [3, 5, 7]
- `learning_rate`: [0.01, 0.1, 0.2]

### 6.2 Method
RandomizedSearchCV (10 iterations) with TimeSeriesSplit (3 folds).

### 6.3 Results
*(Fill in best params from Notebook 04)*

---

## 7. Results, Visualization and Error Analysis (User - 65%)

### 7.1 Test set performance
*(Table comparing Ridge and XGBoost on Test RMSE/MAE)*

### 7.2 Visualization
*(Insert time_series_predictions.png from Notebook 05)*

### 7.3 Error analysis
*(Insert error_vs_meteorology.png from Notebook 05. Discuss the clustering of errors during cold/high-pressure events).*

### 7.4 Answers to your three questions
1. *(Answer Q1 based on u/v feature importance)*
2. *(Answer Q2 based on whether XGBoost degraded with PCA features vs raw)*
3. *(Answer Q3 based on the Error Analysis section)*

---

## 8. Limitations and Next Steps (Mate - 35%)
*(Write about limitations, e.g. spatial interpolation between stations, exogenous variables like traffic data missing).*

---

## 9. Contributions (Mate - 35%)
| Member | Student ID | Contribution |
| :--- | :--- | :--- |
| (Your Name) | (Your ID) | Repository setup, data preprocessing (handling NaNs, target shifting), model training (Ridge, XGBoost), hyperparameter tuning, model evaluation, and error analysis. Report Sections 1, 2, 5, 6, 7. |
| (Mate Name) | (Mate ID) | Data audit, exploratory data analysis, visualizations, feature engineering (lags, PCA, cyclical encoding, wind vectors). Report Sections 3, 4, 8, 9. |
