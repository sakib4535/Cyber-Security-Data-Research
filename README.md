# 🛡️ API Security: Access Behavior and Anomaly Detection With Boosting Algorithms (AdaBoost, Gradient Boost and XGBoost)

Welcome to the Cybersecurity Machine Learning project repository! This project delves into the world of cybersecurity, employing various machine learning algorithms to analyze and interpret data related to security behaviors and patterns.

## 📊 Overview

The primary goal of this project is to leverage machine learning techniques to scrutinize cybersecurity datasets, focusing on features like `inter_api_access_duration(sec)`, `api_access_uniqueness`, `sequence_length(count)`, `vsession_duration(min)`, `ip_type`, `behavior`, `behavior_type`, `num_sessions`, `num_users`, `num_unique_apis`, and more.

## 📈 Analysis Results

# Model Performance 🤖


### AdaBoost Classifier 🚀
- **Best Hyperparameters**: `{'learning_rate': 0.2, 'n_estimators': 200}`
- **Accuracy**: Achieved an accuracy score of 83%.
- **ROC-AUC**: Demonstrated a strong ROC-AUC of 0.93, indicating a robust performance in classification tasks.

### Gradient Boosting Classifier 🔥
- **Best Hyperparameters**: `{'learning_rate': 0.1, 'max_depth': 5, 'min_samples_split': 4, 'n_estimators': 200}`
- **Accuracy**: Attained an accuracy score of 86%.
- **ROC-AUC**: Exhibited a commendable ROC-AUC of 0.94, reflecting excellent discriminative capability between classes.

### XGBoost Classifier 🌟
- **Best Hyperparameters**: `{'learning_rate': 0.1, 'max_depth': 7, 'min_child_weight': 5, 'n_estimators': 200}`
- **Accuracy**: Achieved an accuracy score of 86%.
- **ROC-AUC**: Demonstrated an impressive ROC-AUC of 0.95, showcasing superior performance in distinguishing classes.

These models showcase competitive accuracy and robustness in their ability to classify instances, with XGBoost leading in both accuracy and ROC-AUC among the evaluated algorithms.

### Statistical Analysis 📊

- **Chi-Square Test** 🧮
    - `ip_type`: p-value = 6.58e-50
    - `behavior_type`: p-value = 0.0
    - `source`: p-value = 0.0
    - `type_ip`: p-value = 6.58e-50
    - `type_behaviour`: p-value = 0.0
    - `source_type`: p-value = 0.0

- **T-Test** 📝
    - `inter_api_access_duration(sec)` vs `vsession_duration(min)`: p-value = 1.07e-07

- **Linear Regression** 📈
    - R-squared: 0.153

## 📈 ROC Curve Results

- **AdaBoost**: 0.93
- **Gradient Boosting**: 0.94
- **XGBoost**: 0.95

![Image Description]([Feature_Importance.png))


## 🚀 Getting Started

1. **Clone the repository** to your local machine.
2. **Install the dependencies** specified in `requirements.txt`.
3. **Explore** the notebooks and Python scripts for analysis and model implementation.
4. For more detailed insights, refer to individual files.

## 📌 Note

The provided information serves as a summary. For a comprehensive understanding, refer to specific notebooks and analysis files available within the repository.
