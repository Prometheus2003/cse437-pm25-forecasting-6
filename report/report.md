# CSE437 Data Science: Project Report

## Cover
- **Project title:** Predicting PM2.5 Surges During Winter Inversions
- **CSE437, section 6 , semester:** Summer 2026
- **Group members:** Samiul Mahmud 22299398, Tanvir Ahmmad Jim 22299068
- **GitHub repository link:** https://github.com/Prometheus2003/cse437-pm25-forecasting-6.git
- **Date:** 3 September 2026

## Summary
This project aims to forecast next-hour atmospheric fine particulate matter (PM2.5) concentrations in Beijing. We utilized environmental data from three monitoring stations to engineer temporal lags, rolling windows, and meteorological wind vectors. PCA was applied to mitigate severe multicollinearity among co-pollutants. Our modeling results show that a baseline Ridge Regression heavily outperformed a tuned XGBoost ensemble on the final test set (2017), suggesting that linear models with engineered features may extrapolate better during extreme, unseen winter thermal inversions compared to tree-based methods that tend to overfit the training period.

---

## 1. Problem and Dataset 

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

## 2. Data Handling and Preprocessing 

### 2.1 Data quality audit
An initial audit of the 105,192 rows revealed no duplicate rows. Missing values were present across most features: PM2.5 was missing ~2.36%, while CO had the highest missing rate at ~5.05%. Temporal variables (year, month, day, hour) had no missing values.

### 2.2 Missing values
We assumed missing values were due to sensor downtime. We used linear interpolation (up to 3 hours) for small gaps, and forward filling for larger gaps to preserve temporal continuity without leaking future data.

### 2.3 Outliers
PM2.5 readings had a mean of 73.27 $\mu\text{g}/\text{m}^3$ but reached a maximum of 898.0 $\mu\text{g}/\text{m}^3$. This extreme right skew represents genuine, severe winter pollution events rather than sensor errors, so these outliers were retained.

### 2.4 Transformation and scaling
Scaled using StandardScaler during the PCA pipeline.

### 2.5 Before and after
After loading the raw data, the shape was 105,192 rows. Target shifting (-1 hour) reduced the count to 105,189. After creating 24-hour lag features, the first 24 hours for each station were dropped due to NaNs, resulting in a final shape of 105,117 rows for modeling.

---

## 3. Statistical Analysis 

### 3.1 Descriptive statistics
- **PM2.5:** Mean = 73.27, Std = 76.03, Min = 2.0, Max = 898.0
- **TEMP:** Mean = 13.65°C, Std = 11.38, Min = -16.8°C, Max = 41.4°C
- **PRES:** Mean = 1009.12 hPa, Std = 10.46, Min = 982.4 hPa, Max = 1042.0 hPa

### 3.2 Relationships
A correlation heatmap revealed severe multicollinearity among co-pollutants, specifically PM10, $SO_2$, $NO_2$, and CO. This justified the need for dimensionality reduction.

### 3.3 What the data says so far
- Pollution levels exhibit strong seasonal trends, peaking significantly during the winter months.
- Multicollinearity between co-pollutants suggests they share the same emission sources or weather-driven accumulation conditions.
- The extreme range in PM2.5 concentration indicates that linear modeling alone might struggle without robust feature engineering.

---

## 4. Feature Engineering 

### 4.1 Derived features
Created lag features ($t-1, t-3, t-24$) and 24-hour rolling means to capture temporal dependence without data leakage. Calculated orthogonal wind vectors $u$ and $v$ from speed and direction. Cyclically encoded hour and month using sine/cosine.

### 4.2 Dimensionality reduction
Applied PCA (2 components) to the lagged co-pollutants ($PM10, SO_2, NO_2, CO, O_3$) to remove multicollinearity. The first two principal components captured ~77% (58% + 19%) of the explained variance.

### 4.3 Feature selection
Dropped highly collinear original temporal and spatial features.

### 4.4 Final feature set
The final dataset consists of 65 features, comprising:
- Target and continuous meteorological variables (TEMP, PRES, DEWP, RAIN)
- 1-hour, 3-hour, and 24-hour lags for meteorology and PM2.5
- 24-hour rolling means
- Derived wind vectors ($u\_wind$, $v\_wind$)
- Cyclical time variables ($hour\_sin$, $hour\_cos$, $month\_sin$, $month\_cos$)
- 2 PCA components representing the co-pollutant mixtures ($pollutant\_pca\_1$, $pollutant\_pca\_2$)

---

## 5. Modeling and Validation 

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

## 6. Hyperparameter Tuning 

### 6.1 Search space
- `n_estimators`: [50, 100, 200]
- `max_depth`: [3, 5, 7]
- `learning_rate`: [0.01, 0.1, 0.2]

### 6.2 Method
RandomizedSearchCV (10 iterations) with TimeSeriesSplit (3 folds).

### 6.3 Results
The best XGBoost parameters found were: `{'subsample': 1.0, 'n_estimators': 50, 'max_depth': 3, 'learning_rate': 0.1}`. The best Cross-Validation RMSE was 19.36.

---

## 7. Results, Visualization and Error Analysis 

### 7.1 Test set performance
| Model | Test RMSE | Test MAE | Test R2 |
| :--- | :--- | :--- | :--- |
| **Baseline Ridge** | **23.23** | **11.81** | **0.94** |
| Advanced XGBoost | 77.62 | 74.86 | 0.38 |

Interestingly, the simple Baseline Ridge regression heavily outperformed the advanced XGBoost model on the unseen 2017 test set. This suggests that XGBoost may have overfit to the training period or struggled to extrapolate linear trends during extreme pollution spikes in the 2017 data.

### 7.2 Visualization
*(Refer to `figures/time_series_predictions.png` for a visualization of True vs Predicted PM2.5 during a sample window in Jan 2017)*

### 7.3 Error analysis
An analysis of residuals vs meteorology confirms that the absolute errors of the predictions strongly cluster in regions of low temperature and high pressure. *(Refer to `figures/error_vs_meteorology.png`)*

### 7.4 Answers to your three questions
1. **Wind Vectors:** The decomposition of wind speed and direction into $u$ and $v$ vectors successfully captured the physical mechanics of dispersion vs. accumulation, serving as a critical feature for the linear baseline.
2. **PCA Multicollinearity:** PCA successfully compressed the information of 5 co-pollutants into 2 components (77% variance explained), preventing multicollinearity issues in Ridge Regression while still preserving essential predictive signals.
3. **Seasonal Meteorology Errors:** The highest residual prediction errors occurred during extreme winter thermal inversions (characterized by low temperatures and high atmospheric pressure), where cold air gets trapped near the surface and prevents PM2.5 dispersion. 

---

## 8. Limitations and Next Steps 
Limitations include the absence of exogenous variables, such as local traffic volumes and industrial emissions, which heavily influence localized PM2.5 spikes. Furthermore, spatial interpolation between the three stations was not utilized, limiting the geographic scope of the predictions. Future steps could involve integrating spatial data (e.g., Graph Neural Networks) and incorporating direct emission datasets.

---

## 9. Contributions 
| Member | Student ID | Contribution |
| :--- | :--- | :--- |
| Samiul Mahmud | 22299398 | Repository setup, data preprocessing (handling NaNs, target shifting), model training (Ridge, XGBoost), hyperparameter tuning, model evaluation, and error analysis. Report Sections 1, 2, 5, 6, 7. |
| Tanvir Ahmmad Jim | 22299068 | Data audit, exploratory data analysis, visualizations, feature engineering (lags, PCA, cyclical encoding, wind vectors). Report Sections 3, 4, 8, 9. |
