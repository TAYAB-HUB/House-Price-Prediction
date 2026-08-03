# House Price Prediction — Regularized Linear Regression (from Scratch)

A linear regression model for predicting house prices, implemented from scratch in NumPy — including both Gradient Descent and the Normal Equation, with L2 (Ridge) regularization and a hyperparameter search over the regularization strength (lambda).

## Overview

This project predicts house prices from structural features (lot size, bedrooms, bathrooms, stories, garage spaces) using a regularized linear regression model built without relying on scikit-learn's estimator classes. Both classical solution methods for linear regression are implemented and compared:

1. **Gradient Descent** — iterative weight updates with an L2 penalty term
2. **Normal Equation** — closed-form solution with a regularization term added to the design matrix

For each method, the model is trained and evaluated across a range of lambda (regularization strength) values from 0 to 600 to find the value that minimizes prediction error on the test set.

## Dataset

- **File:** `Housing_Price_dataset.csv`
- **Records:** ~546 houses
- **Features used:** `lotsize`, `bedrooms`, `bathrms`, `stories`, `garagepl`
- **Target:** `price`
- **Dropped columns:** `driveway`, `recroom`, `fullbase`, `airco`, `prefarea`, `gashw` (categorical yes/no features excluded from this version)

## Tech Stack

- Python
- NumPy
- Pandas
- Matplotlib

## Methodology

1. **Feature scaling** — all features and the target are standardized (z-score normalization: subtract mean, divide by standard deviation)
2. **Train/test split** — 90/10 split (no shuffling — sequential split on the ordered dataset)
3. **Bias term** — a column of ones is prepended to the feature matrix for the intercept
4. **Cost function** — Mean Squared Error with an added L2 regularization term (bias term excluded from the penalty)
5. **Gradient Descent** — 500 iterations, learning rate `alpha = 0.1`, run once per lambda value across the 0–600 range
6. **Normal Equation** — closed-form `θ = (XᵀX + λI)⁻¹XᵀY`, also swept across the same lambda range (bias term excluded from the penalty matrix)
7. **Evaluation metric** — mean absolute percentage error (MAPE) between denormalized predicted and actual prices
8. **Hyperparameter selection** — the lambda that minimizes test-set error is selected as optimal, separately for each method

## Results

### Gradient Descent

| Metric | Value |
|---|---|
| Optimal lambda | 24 |
| Minimum error | 13.96% |

![Lambda vs Error - Gradient Descent](Error_vs_lambda.png)

### Normal Equation

| Metric | Value |
|---|---|
| Optimal lambda | 311 |
| Minimum error | 13.43% |

![Lambda vs Error - Normal Equation](lambda_vs_Error.png)

### Interpretation

- Both methods land in a similar error range (~13–14% MAPE), with the Normal Equation finding a marginally better minimum.
- The two error curves have a classic U-shape: too little regularization (low lambda) underfits less but generalizes worse, while too much regularization (high lambda) oversimplifies the model and error rises again.
- The very different optimal lambda values (24 vs. 311) between the two methods reflect differences in how each optimization approach interacts with the penalty term — Gradient Descent's penalty is scaled relative to the number of training iterations and learning rate, while the Normal Equation applies it directly in closed form, so their effective regularization strength isn't directly comparable.

## Known Issues

- The notebook currently references a case-mismatched variable (`Mean` vs `mean`) during normalization and reads the CSV under a different filename (`Housing Price data set.csv`) than the one included here (`Housing_Price_dataset.csv`) — update these before re-running end-to-end.
- Only numeric features are used; the dropped categorical features (`airco`, `prefarea`, `driveway`, etc.) likely carry real predictive signal and are worth reintroducing with one-hot encoding.

## Future Improvements

- Fix the filename/variable issues above so the notebook runs top-to-bottom without manual edits
- One-hot encode the excluded categorical features and re-evaluate
- Add k-fold cross-validation instead of a single 90/10 sequential split
- Compare against scikit-learn's `Ridge` and `LinearRegression` as a sanity check on the from-scratch implementation
- Report R² alongside MAPE for a fuller picture of fit quality

## Project Structure

```
├── House_Preiction_Linear_Regression.ipynb   # Main notebook: preprocessing, model, training, evaluation
├── Housing_Price_dataset.csv                  # Dataset
├── Error_vs_lambda.png                        # Gradient Descent: lambda vs error
├── lambda_vs_Error.png                         # Normal Equation: lambda vs error
└── README.md
```

## Usage

```bash
pip install numpy pandas matplotlib
jupyter notebook House_Preiction_Linear_Regression.ipynb
```

## Author

**Syed Mohammed Tayab**
[GitHub](https://github.com/TAYAB-HUB) | [LinkedIn](https://linkedin.com/in/syed-tayab01)
