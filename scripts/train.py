from sklearn.ensemble import RandomForestClassifier
from joblib import dump
from data_prep import load_data, preprocess_data, split_data, scale_data

def train_model(X_train, y_train):
    """Train a RandomForest model."""
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

if __name__ == "__main__":
    # Load and preprocess data
    file_path = "data/raw/donnees-defi-egc.csv"
    data = load_data(file_path)
    processed_data = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(processed_data, "DEFAUT")
    X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
    
    # Train model
    model = train_model(X_train_scaled, y_train)
    
    # Save model
    dump(model, "models/random_forest_model.pkl")
    print("Model saved to models/random_forest_model.pkl")
