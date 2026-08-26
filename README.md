# cse437-pm25-forecasting-6

## Problem Statement
We are building a time-series regression model to predict atmospheric fine particulate matter concentration (PM2.5) in Beijing. Given the health implications of high PM2.5 levels, accurate forecasting is critical. We are forecasting the **next hour ($t+1$) PM2.5 concentration** based on historical data.

## Dataset
**Name:** Beijing Multi-Site Air-Quality Data Set
**Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data)
**Size:** 420,768 hourly observations across 12 monitoring stations (2013–2017) with 18 features. We have filtered this to 3 stations (Aotizhongxin, Changping, and Dingling) as per project requirements.
**Target Variable:** PM2.5 continuous numerical value ($\mu\text{g}/\text{m}^3$).

## Three Research Questions
1. How do orthogonal wind vector components ($u$ and $v$) and barometric pressure interact to drive local particulate accumulation versus atmospheric dispersion?
2. Can feature selection and dimensionality reduction (PCA) resolve severe multicollinearity among co-pollutants ($SO_2, NO_2, CO, O_3$) without degrading the model's predictive power during sudden pollution surges?
3. Under what seasonal meteorological conditions (such as winter thermal inversions) does the regression model exhibit its highest residual prediction errors, and why?

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run notebooks sequentially:
   - `notebooks/01_data_audit_and_eda.ipynb`
   - `notebooks/02_preprocessing.ipynb`
   - `notebooks/03_feature_engineering.ipynb`
   - `notebooks/04_modeling_and_tuning.ipynb`
   - `notebooks/05_evaluation_and_error_analysis.ipynb`
