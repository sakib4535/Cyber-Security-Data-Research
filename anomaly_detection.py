# -*- coding: utf-8 -*-
"""Anomaly_Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RASsCURiPC64Qd0p85pfP23vBF26m82S
"""



"""# **API Security: Access Behavior and Anomaly Detection With Boosting Algorithms (AdaBoost, Gradient Boost and XGBoost)**

Microservice-based applications are commonly accessed through APIs, utilized by both applications and direct programmatic calls. Attackers often exploit these APIs by manipulating the exposed business logic. User access patterns differ significantly between normal users and attackers. Applications may have hundreds of APIs called in a specific sequence, and these behaviors can vary for the same user due to factors such as browser refreshes, session refreshes, network errors, or programmatic access. API calls in long-running sessions form access graphs that need to be analyzed to identify attack patterns and anomalies. However, graphs are not well-suited for numerical computations. To address this challenge, we provide a dataset where user access behavior is transformed into quantitative features. Additionally, we provide a dataset containing raw API call graphs. To support the use of these datasets, two notebooks on classification, node embeddings, and clustering are also included.

Here's an analysis of each column in the dataset might be useful in a cybersecurity context:

1. **`inter_api_access_duration(sec)`:**
   - **Use:** Measures the duration of interaction between APIs. Unusual deviations from typical interaction times could signal anomalies or potential attacks.

2. **`api_access_uniqueness`:**
   - **Use:** Represents the uniqueness or diversity of API access patterns. Uncommon or highly unique access patterns might indicate suspicious behavior or attempts to access restricted APIs.

3. **`sequence_length(count)`:**
   - **Use:** Indicates the length of API call sequences. Unusual or exceptionally long sequences might signify complex operations or potential threats.

4. **`vsession_duration(min)`:**
   - **Use:** Captures the duration of virtual sessions. Abnormally long sessions or very short sessions might indicate potential security risks or anomalies.

5. **`ip_type`:**
   - **Use:** Classifies the type of IP addresses (e.g., public, private, VPN). It helps identify the origin or nature of connections and can be used to flag suspicious IP types.

6. **`num_sessions`, `num_users`, `num_unique_apis`:**
   - **Use:** Counts the number of sessions, unique users, and unique APIs involved in interactions. Unusually high or low counts might suggest abnormal behavior or potential threats.

7. **`source`:**
   - **Use:** Represents the source of API interactions. Different sources (e.g., internal, external, specific devices) can help track and identify where potential threats or anomalies originate.

8. **`classification`:**
   - **Use:** This likely represents the labeled classes (e.g., 'malicious' vs. 'benign') for supervised learning. It's the target variable for predictive modeling to train algorithms to identify and classify cybersecurity events.

These columns provide valuable insights and features for building machine learning models aimed at cybersecurity applications. They capture various aspects of interactions, durations, patterns, and categorizations that are crucial in detecting, preventing, and responding to potential security threats and anomalies within a system or network.
"""

import pandas as pd
import polars as ps
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import sys
from google.colab import files
import pandas as pd
import io

from scipy.stats import ttest_ind, chi2_contingency
import statsmodels.api as sm

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, train_test_split, learning_curve
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
import xgboost as xgb
from sklearn.metrics import accuracy_score, confusion_matrix, roc_curve, auc, classification_report
from sklearn.tree import DecisionTreeClassifier, plot_tree

uploaded = files.upload()

uploaded2 = files.upload()

filename = "supervised_dataset.csv"

if filename in uploaded:
  data = pd.read_csv(io.StringIO(uploaded[filename].decode('utf-8')))
  print(data.head())
else:
  print("the File Doesn't Exists")

filename = "remaining_behavior_ext.csv"

if filename in uploaded2:
  data_remain = pd.read_csv(io.StringIO(uploaded2[filename].decode('utf-8')))
  print(data_remain.head())
else:
  print("the File Doesn't Exists")

data.head(10)

data.columns

data.info()

data.describe()

data.isnull().sum()

plt.figure(figsize=(8,6))
sns.heatmap(data.isnull(), cmap='Greys', cbar=False)
plt.title("Null Data Heatmap")
plt.show()

# columns_to_drop = [
#
# ]

# df = data[columns_to_drop].copy()

# data.drop(columns=columns_to_drop, inplace=True)
# print("Modified Original DataFrame:")
# print(data.head())

# print("\nNew DataFrame 'df':")
# print(df.head())

data_remain['inter_api_access_duration(sec)'].fillna(method='ffill', inplace=True)
data_remain['api_access_uniqueness'].fillna(method='ffill', inplace=True)

data_remain.isnull().sum()





"""# **Exploratory Data Analysis (EDA):**"""



data.info()

data_remain.info()

print(data_remain['inter_api_access_duration(sec)'].describe())

# Histogram for 'Packet Length'
plt.figure(figsize=(8, 6))
plt.hist(data_remain['inter_api_access_duration(sec)'], bins=30, color='skyblue', edgecolor='black')
plt.xlabel('inter_api_access_duration(sec)')
plt.ylabel('Frequency')
plt.title('Distribution of Inter API Access Duration')
plt.show()

"""**`"Inter API Access Duration" `**typically refers to the period during which an application or service has access to another application's programming interface (API) to retrieve or manipulate data.

For instance, when an application uses an API provided by another service (like accessing weather data from a weather service), the access duration refers to how long the first application can continue to utilize that API before it needs to renew or re-authenticate its access.
"""

# Top 20 access uniqueness
top_20_access_uniqueness = data_remain['api_access_uniqueness'].value_counts().head(20)

colors = ['blue', 'green', 'red', 'magenta', 'orange', 'pink', 'yellow']
# 'Packet Type' frequencies
plt.figure(figsize=(10, 6))
top_20_access_uniqueness.plot(kind='bar', color=colors)
plt.xlabel('api_access_uniqueness')
plt.ylabel('Count')
plt.title('Top 20 api_access_uniqueness Distribution')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

"""Measuring **API access uniqueness** involves assessing how distinct or varied the usage patterns are across different API access instances or users. It aims to quantify the diversity or individuality within the API usage.

Monitoring uniqueness helps detect unusual or unauthorized access patterns, which could indicate security breaches or misuse. Understanding how diverse API access is can help allocate resources better. For instance, identifying popular versus less-used endpoints can aid in resource optimization.
"""

# Create a histogram for 'vsession_duration(min)'
plt.figure(figsize=(10, 6))
data_remain['vsession_duration(min)'].hist(bins=20, edgecolor='black', alpha=0.7)
plt.xlabel('Vsession Duration (min)')
plt.ylabel('Count')
plt.title('Distribution of Vsession Duration')
plt.grid(True)
plt.tight_layout()
plt.show()



"""**"Vsession Duration (min)"** typically refers to the duration of a virtual session measured in minutes. This metric quantifies the amount of time a user or a system remains actively engaged or connected within a virtual environment, platform, or system.

 Longer Vsession Durations often indicate higher user engagement or prolonged usage of a platform or service, which can be an essential metric for evaluating the success or popularity of an online platform.
"""

plt.figure(figsize=(17,6))
corr = data_remain.corr(method='kendall')
map = np.triu(corr)
sns.heatmap(corr, mask=map, annot=True, cmap='Set2')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(data=data, x='source', palette='colorblind')
plt.xlabel('Sources')
plt.ylabel('Count')
plt.title('Distribution of Source Network System')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



"""## **Feature Transformation**"""

# Label Encoding

label = LabelEncoder()

data_remain['type_ip'] = label.fit_transform(data_remain['ip_type'])
data_remain['type_behaviour'] = label.fit_transform(data_remain['behavior_type'])
data_remain['source_type'] = label.fit_transform(data_remain['source'])
data_remain['behaviour']= label.fit_transform(data_remain['behavior'])

# Splitting Training-Testing-Validation Sets
x=data_remain[['inter_api_access_duration(sec)','api_access_uniqueness', 'sequence_length(count)','vsession_duration(min)','type_behaviour' ,'behaviour','num_sessions', 'num_users', 'num_unique_apis']]
y=data_remain['source_type']
x_train,x_test,y_train,y_test=train_test_split(x,y)

data_remain.info()

x_train.shape

y_train.shape

x_test.shape

y_test.shape

numerical_columns = ['inter_api_access_duration(sec)', 'vsession_duration(min)']

# Handling missing values by replacing them with zeros
data[numerical_columns] = data[numerical_columns].fillna(0)

# T-test for two numerical columns
t_stat, p_val = ttest_ind(data['inter_api_access_duration(sec)'], data['vsession_duration(min)'])
print(f"T-test p-value: {p_val}")
# Correlation analysis
correlation_matrix = data.corr()

# Categorical analysis
categorical_columns = ['ip_type', 'behavior', 'behavior_type', 'source', 'type_ip', 'type_behaviour', 'source_type', 'behaviour']
for col in categorical_columns:
    print(data_remain[col].value_counts())  # Frequency analysis
    contingency_table = pd.crosstab(data_remain[col], data_remain['source_type'])  # Replace 'target_column' with your dependent variable
    chi2, p, _, _ = chi2_contingency(contingency_table)
    print(f"Chi-square p-value for {col}: {p}")

# Inferential analysis (example - t-test for two numerical columns)
t_stat, p_val = ttest_ind(data['inter_api_access_duration(sec)'], data['vsession_duration(min)'])
print(f"T-test p-value: {p_val}")

# Linear regression example
X = data_remain[['num_sessions', 'num_users', 'num_unique_apis', 'inter_api_access_duration(sec)', 'api_access_uniqueness', 'sequence_length(count)']]
y = data_remain['source_type']
X = sm.add_constant(X)  # Adding constant for the intercept term
model = sm.OLS(y, X).fit()
print(model.summary())



"""## **Inferential Statistical Analysis of the Result Given by Ordinary Least Squares For all Features Given in the dataset**

### T-test:
- The T-test between **`'inter_api_access_duration(sec)'`** and **`'vsession_duration(min)'`** yielded a p-value of 1.07e-07, indicating a statistically significant difference between these two variables. This suggests that these two variables might have differing impacts on the 'source_type'.

### Chi-square tests:
- **ip_type, behavior, behavior_type, source, type_ip, type_behaviour, source_type, and behaviour:**
  - All of these categorical variables exhibit highly significant associations with the **`'source_type'`** (p-values close to zero). This implies that these categorical variables are potentially strong predictors or indicators of the 'source_type'.

### OLS Regression:
- The regression model with predictors `**num_sessions**`, `**num_users**`, `**num_unique_apis**`,** `inter_api_access_duration(sec)`** , **Inline code**, `**api_access_uniqueness**`, and `**sequence_length(count)**` explains approximately 15.3% of the variance in the 'source_type'.
- Individual predictors:
  - **num_sessions, num_users, num_unique_apis, inter_api_access_duration(sec), api_access_uniqueness, and sequence_length(count):**
    - All of these predictors show statistically significant coefficients (p-values close to zero), indicating that each has a significant impact on predicting the 'source_type' when considered independently.
  - **const (intercept term):**
    - The intercept term is also statistically significant, suggesting that even without any predictors, there exists a baseline effect on the 'source_type'.
- The model's **low R-squared value (15.3%)** indicates that while these predictors significantly contribute to explaining the 'source_type', a substantial portion of the variability in 'source_type' remains unexplained by this model.

### Overall Analysis:
- The findings indicate that both numerical and categorical variables have strong relationships with the target variable 'source_type'. However, while the relationships are statistically significant, the explanatory power of the model remains moderate (R-squared of 15.3%). Other unexplored factors may contribute to the variability in 'source_type' not accounted for by these variables.
"""



"""### **Hyperparameter Tuning and Setting Up Boosting Algorithms (AdaBoost, Gradient Boost, XGBoost)**"""

# Define the hyperparameter search space
ada_params = {
    'n_estimators': [50, 100, 200], #  representing the number of estimators (decision trees) in the AdaBoost ensemble
    'learning_rate': [0.01, 0.1, 0.2] # learning rate of the AdaBoost algorithm, controlling the contribution of each classifier in the ensemble.
}

# Train and evaluate the AdaBoostClassifier model using GridSearchCV
ada_clf = AdaBoostClassifier(random_state=42)
ada_grid = GridSearchCV(ada_clf, ada_params, error_score='raise', cv=5, scoring='accuracy')
ada_grid.fit(x_train, y_train)

# Print the best hyperparameters for AdaBoost
print("Best Hyperparameters for AdaBoost:", ada_grid.best_params_)

# Define the hyperparameter search space
gb_params = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 4, 6]
}

gb_clf = GradientBoostingClassifier(random_state=42)
gb_grid = GridSearchCV(gb_clf, gb_params, cv=5, scoring='accuracy')
gb_grid.fit(x_train, y_train)

# Print the best hyperparameters for Gradient Boosting
print("Best Hyperparameters for Gradient Boosting:", gb_grid.best_params_)

# Define the hyperparameter search space
xgb_params = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 5, 7],
    'min_child_weight': [1, 3, 5]
}

xgb_clf = xgb.XGBClassifier(random_state=42)
xgb_grid = GridSearchCV(xgb_clf, xgb_params, cv=5, scoring='accuracy')
xgb_grid.fit(x_train, y_train)

# Print the best hyperparameters for XGBoost
print("Best Hyperparameters for XGBoost:", xgb_grid.best_params_)

# Evaluate the models on the testing set
ada_predictions = ada_grid.best_estimator_.predict(x_test)
gb_predictions = gb_grid.best_estimator_.predict(x_test)
xgb_predictions = xgb_grid.best_estimator_.predict(x_test)

# Evaluate accuracy
ada_accuracy = accuracy_score(y_test, ada_predictions)
gb_accuracy = accuracy_score(y_test, gb_predictions)
xgb_accuracy = accuracy_score(y_test, xgb_predictions)

# Evaluation metrics
ada_report = classification_report(y_test, ada_predictions)
gb_report = classification_report(y_test, gb_predictions)
xgb_report = classification_report(y_test, xgb_predictions)

ada_confusion_matrix = confusion_matrix(y_test, ada_predictions)
gb_confusion_matrix = confusion_matrix(y_test, gb_predictions)
xgb_confusion_matrix = confusion_matrix(y_test, xgb_predictions)


print(f"Accuracy for AdaBoost: {ada_accuracy:.2f}")
print(f"Accuracy for Gradient Boosting: {gb_accuracy:.2f}")
print(f"Accuracy for XGBoost: {xgb_accuracy:.2f}")

# Additional metrics and information
print("\nClassification Report for AdaBoost:")
print(ada_report)
print("\nConfusion Matrix for AdaBoost:")
print(ada_confusion_matrix)

print("\nClassification Report for Gradient Boosting:")
print(gb_report)
print("\nConfusion Matrix for Gradient Boosting:")
print(gb_confusion_matrix)

print("\nClassification Report for XGBoost:")
print(xgb_report)
print("\nConfusion Matrix for XGBoost:")
print(xgb_confusion_matrix)

"""## **Accuracy Test Result**


"""

models = ['AdaBoost', 'Gradient Boosting', 'XGBoost']
accuracies = [ada_accuracy, gb_accuracy, xgb_accuracy]

plt.figure(figsize=(8,6))
plt.bar(models, accuracies, color=['blue', 'green', 'orange'])
plt.xlabel('Models')
plt.ylabel('Accuracy')
plt.title("Accuracy Comparison of Models")
plt.ylim(0, 1)
plt.show()

plt.figure(figsize=(15, 5))

# Confusion Matrix for AdaBoost
plt.subplot(1, 3, 1)
sns.heatmap(ada_confusion_matrix, annot=True, cmap='Blues', fmt='d', cbar=False)
plt.title('Confusion Matrix - AdaBoost')

# Confusion Matrix for Gradient Boosting
plt.subplot(1, 3, 2)
sns.heatmap(gb_confusion_matrix, annot=True, cmap='Greens', fmt='d', cbar=False)
plt.title('Confusion Matrix - Gradient Boosting')

# Confusion Matrix for XGBoost
plt.subplot(1, 3, 3)
sns.heatmap(xgb_confusion_matrix, annot=True, cmap='Oranges', fmt='d', cbar=False)
plt.title('Confusion Matrix - XGBoost')

plt.tight_layout()
plt.show()

"""### **Finding Feature Importance and Hyperparameter Sensitivity for All Boosting Algorithms**"""

ada_model = AdaBoostClassifier(**ada_grid.best_params_, random_state=42)
gb_model = GradientBoostingClassifier(**ada_grid.best_params_, random_state=42)
xgb_model = xgb.XGBClassifier(**ada_grid.best_params_, random_state=42)

models = [ada_model, gb_model, xgb_model]
model_names = ['AdaBoost', 'Gradient Boosting', 'XGBoost']
params=[ada_params, gb_params, xgb_params]
features = ['inter_api_access_duration(sec)', 'api_access_uniqueness', 'sequence_length(count)',
            'vsession_duration(min)', 'type_behaviour', 'behaviour', 'num_sessions',
            'num_users', 'num_unique_apis']

plt.figure(figsize=(18,12))
for i, model in enumerate(models):
  # Feature Importance Extraction Process
  model.fit(x_train, y_train)
  feature_importance = model.feature_importances_

  plt.subplot(3 , 3, i*3 + 1)
  plt.barh(features, feature_importance, color=['skyblue', 'lightgreen', 'salmon'][i])
  plt.xlabel('Feature Importance')
  plt.ylabel('Features')
  plt.title(f'Feature Importance - {model_names[i]}')


  # Model Interpretability (if applicable)
  if model_names[i] != 'XGBoost':
    plt.subplot(3, 3, i*3 + 2)
    if hasattr(model, 'estimators_'):
      for est in model.estimators_:
        if hasattr(est, 'tree_'):
          plot_tree(est, filled=True, feature_names=features)  # Visualize The Tree
          plt.title(f"Decision Tree Visualization - {model_names[i]}")


  # Hyper Parameter Sensitivity Check For All Three Boosting Algorithm
  plt.subplot(3, 3, i*3 + 3)
  test_accuracies = []
  for param in params[i]['n_estimators']:
    model.set_params(**{list(params[i].keys())[0]: param})
    model.fit(x_train, y_train)
    test_accuracy = model.score(x_test, y_test)
    test_accuracies.append(test_accuracy)

  plt.plot(params[i]['n_estimators'], test_accuracies, marker='o')
  plt.xlabel('Number of Estimators')
  plt.ylabel('Test Accuracy')
  plt.title(f"{model_names[i]}: Hyperparameter Sensitivity")

plt.tight_layout()
plt.show()

models = [ada_grid.best_estimator_, gb_grid.best_estimator_, xgb_grid.best_estimator_]
model_names = ['AdaBoost', 'Gradient Boosting', 'XGBoost']

plt.figure(figsize=(12, 6))

for model, name in zip(models, model_names):
  train_sizes, train_scores, val_scores = learning_curve(model, x_train, y_train, cv=5, scoring='accuracy')
  train_mean = np.mean(train_scores, axis=1)
  val_mean = np.mean(val_scores, axis=1)
  plt.plot(train_sizes, train_mean, label=f'{name} - Training', marker='o')
  plt.plot(train_sizes, val_mean, label=f'{name} - Validation', marker='o')

plt.xlabel('Training Size')
plt.ylabel('Accuracy')
plt.title('Learning Curve')
plt.legend()
plt.grid()
plt.show()

"""### **Plotting ROC-AUC Curve**

**`ROC-AUC (Receiver Operating Characteristic - Area Under Curve)`** is a useful metric for understanding the discriminative power of a binary classifier. It illustrates the classifier's ability to distinguish between classes by plotting the trade-off between true positive rate (sensitivity) and false positive rate (1 - specificity) across various thresholds.

Boosting algorithms often excel in handling imbalanced datasets where one class dominates the other. ROC-AUC is a preferred metric in such cases as it's less affected by class imbalance and provides a comprehensive view of classifier performance across different thresholds.
"""

plt.figure(figsize=(8, 6))
