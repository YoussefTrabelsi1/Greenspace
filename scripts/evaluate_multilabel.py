from sklearn.metrics import hamming_loss, classification_report
from joblib import load
from data_prep import load_data, preprocess_data, split_multilabel_data, scale_data

def evaluate_multilabel_model(model, X_test, y_test):
    """Evaluate the multi-label model's performance."""
    y_pred = model.predict(X_test)
    # Hamming Loss
    print("Hamming Loss:", hamming_loss(y_test, y_pred))
    
    # Classification Report for each label
    print("\nClassification Report for Multi-label Classification:\n")
    for idx, col in enumerate(y_test.columns):
        print(f"Label: {col}")
        print(classification_report(y_test[col], y_pred[:, idx]))
        print("-" * 30)

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
    
    # Load model
    model = load(model_path)
    
    # Evaluate model
    evaluate_multilabel_model(model, X_test_scaled, y_test)
