from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from joblib import dump
from data_prep import load_data, preprocess_data, split_multilabel_data, scale_data

def train_multilabel_model(X_train, y_train):
    """Train a multi-label RandomForest model."""
    base_model = RandomForestClassifier(random_state=42)
    multilabel_model = MultiOutputClassifier(base_model)
    multilabel_model.fit(X_train, y_train)
    return multilabel_model

if __name__ == "__main__":
    # File paths
    file_path = "data/raw/donnees-defi-egc.csv"
    target_cols = ["Collet", "Houppier", "Racine", "Tronc"]  # Multi-label targets
    model_path = "models/multilabel_random_forest.pkl"

    # Load and preprocess data
    data = load_data(file_path)
    processed_data = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_multilabel_data(processed_data, target_cols)
    X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
    
    # Train multi-label model
    model = train_multilabel_model(X_train_scaled, y_train)
    
    # Save model
    dump(model, model_path)
    print(f"Multi-label model saved to {model_path}")
