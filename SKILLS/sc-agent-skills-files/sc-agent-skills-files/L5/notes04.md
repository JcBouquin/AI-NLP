# Practice Questions for Machine Learning Models

## Instructions

These practice questions are designed to test your understanding of the material covered in the Machine Learning Models lecture. Work through each question carefully and show your reasoning.

---

## Part 1: True/False Questions

**Question 1:** In a machine learning model, the independent variables are the features and the dependent variable is the label.

**Question 2:** Parametric models have a fixed number of parameters that is independent of the number of training examples.

**Question 3:** In linear regression, the equation y = x^T w + w_0 represents a hyperplane in the feature space.

**Question 4:** A model with high complexity on non-linearly separable data will always outperform a simple linear model because it can capture more complex patterns.

**Question 5:** Non-parametric models have no parameters at all, which is why they are called "non-parametric".

---

## Part 2: Explanatory Questions

**Question 6:** Describe the relationship between model input, model parameters, and model output in the context of supervised machine learning. How do these three components interact during the training phase versus the prediction phase?

**Question 7:** Compare and contrast parametric and non-parametric machine learning models. Include in your discussion: (a) how they differ in their assumptions about the mapping function, (b) how the number of training examples affects each type, and (c) provide one example of each type from the lecture.

**Question 8:** Explain the geometric interpretation of linear classification models. What does the equation x^T w + w_0 = 0 represent, and what role does the weight vector w play in this geometric interpretation?

**Question 9:** What are the main advantages and disadvantages of linear models? Under what circumstances would a linear model be most appropriate, and when might it fail to capture the underlying relationship in the data?

**Question 10:** Explain the goal of the training phase for linear models. For simple linear regression, describe how the parameters w_1 and w_0 affect the fitted line geometrically, and what criterion is used to select the best values for these parameters.

---

## Part 3: Coding Question

**Question 11: Implementing Simple Linear Regression from Scratch**

Implement a simple linear regression model from scratch that finds the best-fit line for a dataset by minimizing the sum of squared errors (residuals). Your implementation should compute the optimal weights using the closed-form solution.

**Steps:**
1. Implement a function to compute predictions given features, weights, and intercept
2. Implement a function to compute the sum of squared errors between predictions and actual labels
3. Implement a function to fit the linear regression model by computing optimal parameters
4. Test your implementation on sample data and visualize the results

**Function Signatures:**

```python
import numpy as np
import matplotlib.pyplot as plt

def predict(X, w_1, w_0):
    """
    Compute predictions using the linear model
    
    Args:
        X: numpy array of shape (n,) containing feature values
        w_1: float, the weight (slope) parameter
        w_0: float, the intercept parameter
    
    Returns:
        numpy array of shape (n,) containing predictions
    """
    pass

def compute_sse(y_true, y_pred):
    """
    Compute the sum of squared errors
    
    Args:
        y_true: numpy array of shape (n,) containing true labels
        y_pred: numpy array of shape (n,) containing predicted labels
    
    Returns:
        float: sum of squared errors
    """
    pass

def fit_simple_linear_regression(X, y):
    """
    Fit simple linear regression model using the closed-form solution
    
    For simple linear regression: y = w_1 * x + w_0
    Optimal parameters minimize SSE = sum((y_i - (w_1*x_i + w_0))^2)
    
    Args:
        X: numpy array of shape (n,) containing feature values
        y: numpy array of shape (n,) containing labels
    
    Returns:
        tuple: (w_1, w_0) the optimal weight and intercept
    """
    pass
```

**Example:**

```python
# Generate sample data
np.random.seed(42)
X = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
y = np.array([2.1, 3.9, 6.2, 8.1, 9.8, 12.0])

# Fit the model
w_1, w_0 = fit_simple_linear_regression(X, y)

# Make predictions
y_pred = predict(X, w_1, w_0)

# Compute error
sse = compute_sse(y, y_pred)

print(f"Optimal weight (slope): {w_1:.3f}")
print(f"Optimal intercept: {w_0:.3f}")
print(f"Sum of Squared Errors: {sse:.3f}")

# Expected output (approximate):
# Optimal weight (slope): 1.971
# Optimal intercept: 0.086
# Sum of Squared Errors: 0.327
```

**Hints:**
- For simple linear regression, the optimal parameters can be computed using: w_1 = cov(X, y) / var(X) and w_0 = mean(y) - w_1 * mean(X)
- The sum of squared errors is also called the residual sum of squares (RSS)
- Remember that predictions are computed as: y_pred = w_1 * X + w_0
- You can use numpy functions like `np.mean()`, `np.var()`, and `np.cov()` to compute statistics
- To visualize, plot the original data points as scatter plot and overlay the fitted line

---

## Part 4: Use Case Application

**Question 12: Predicting Student Graduate School Admission**

**Scenario:**

You are a data scientist working for an educational consulting company. The company wants to help prospective graduate school applicants understand their chances of admission based on their test scores. You have been provided with historical data of students including their GRE scores (Graduate Record Examination), TOEFL scores (Test of English as a Foreign Language), and whether they were admitted to graduate school (0 = not admitted, 1 = admitted). Your task is to build a linear classification model to predict admission status.

**Data:**

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

# Generate sample data (similar to the lecture example)
np.random.seed(42)
n_samples = 200

# Generate GRE scores (260-340 range)
gre_scores = np.random.normal(310, 15, n_samples)
gre_scores = np.clip(gre_scores, 260, 340)

# Generate TOEFL scores (90-120 range)
toefl_scores = np.random.normal(105, 8, n_samples)
toefl_scores = np.clip(toefl_scores, 90, 120)

# Generate admission status (higher scores = higher probability of admission)
# Create a weighted sum with some noise
admission_score = 0.05 * gre_scores + 0.08 * toefl_scores + np.random.normal(0, 2, n_samples)
admission = (admission_score > 17).astype(int)

# Create DataFrame
data = pd.DataFrame({
    'GRE': gre_scores,
    'TOEFL': toefl_scores,
    'Admitted': admission
})

print(data.head())
print(f"\nAdmission rate: {admission.mean():.2%}")
```

**Task:**

Build and evaluate a logistic regression model (a linear classification model) to predict graduate school admission based on GRE and TOEFL scores. Your solution should include data preprocessing, model training, evaluation, and visualization of the decision boundary.

**Requirements:**
- Split the data into training (80%) and test (20%) sets
- Standardize the features before training (remember: fit the scaler on training data only!)
- Train a logistic regression model on the training data
- Evaluate the model on the test set using accuracy and confusion matrix
- Create a visualization showing the data points (colored by actual admission status) and the linear decision boundary learned by the model
- Interpret the model coefficients: which feature (GRE or TOEFL) has a stronger influence on admission prediction?

**Hints:**
- Use `StandardScaler` to normalize features - this helps logistic regression converge faster and makes coefficient interpretation easier
- The decision boundary for logistic regression is the line where x^T w + w_0 = 0, or equivalently: w_1 * x_1 + w_2 * x_2 + w_0 = 0
- To plot the decision boundary, rearrange the equation to solve for x_2 in terms of x_1: x_2 = -(w_1 * x_1 + w_0) / w_2
- Remember to apply the same standardization transformation to the test set using the scaler fitted on training data
- The magnitude of the coefficients (after standardization) indicates feature importance
- A confusion matrix will help you understand if the model has bias toward predicting one class over another
