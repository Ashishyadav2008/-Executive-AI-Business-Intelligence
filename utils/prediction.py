import numpy as np
from sklearn.linear_model import LinearRegression

def predict_sales(df):
    """
    Generic prediction function
    Works with ANY numeric column
    """

    # Select numeric columns
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if not numeric_cols:
        return None

    # Pick best column (highest variance)
    target_col = max(numeric_cols, key=lambda c: df[c].var())

    # Drop NaN values
    y = df[target_col].dropna()

    if len(y) < 2:
        return None

    # Create index-based X
    X = np.arange(len(y)).reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    future_index = np.array([[len(y)]])
    prediction = model.predict(future_index)[0]

    return {
        "column": target_col,
        "predicted_value": round(float(prediction), 2)
    }
