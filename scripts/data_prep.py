import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(file_path):
    """Load dataset from a CSV file."""
    return pd.read_csv(file_path)

def preprocess_data(data):
    """Handle missing values and encode categorical data."""
    # Fill missing values
    data = data.ffill()

    # Encode categorical features
    categorical_cols = data.select_dtypes(include=['object']).columns
    data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
    
    return data

def split_data(data, target_col):
    """Split data into training and test sets."""
    X = data.drop(columns=[target_col])
    y = data[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    return X_train, X_test, y_train, y_test

def split_multilabel_data(data, target_cols):
    """Split data into training and test sets for multi-label classification."""
    X = data.drop(columns=target_cols)
    y = data[target_cols]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def scale_data(X_train, X_test):
    """Scale data using StandardScaler."""
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, scaler

if __name__ == "__main__":
    # File paths
    file_path = "data/raw/donnees-defi-egc.csv"
    target_cols = ["Collet", "Houppier", "Racine", "Tronc"]  # Multi-label targets

    # Load and preprocess data
    data = load_data(file_path)
    processed_data = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_multilabel_data(processed_data, target_cols)
    X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
