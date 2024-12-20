from sklearn.metrics import accuracy_score, classification_report
from joblib import load
from data_prep import load_data, preprocess_data, split_data, scale_data

def evaluate_model(model, X_test, y_test):
    """Evaluate the model's performance."""
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

if __name__ == "__main__":
    # Load and preprocess data
    file_path = "data/raw/donnees-defi-egc.csv"
    data = load_data(file_path)
    processed_data = preprocess_data(data)
    X_train, X_test, y_train, y_test = split_data(processed_data, "DEFAUT")
    X_train_scaled, X_test_scaled, scaler = scale_data(X_train, X_test)
    
    # Load model
    model = load("models/random_forest_model.pkl")
    
    # Evaluate model
    evaluate_model(model, X_test_scaled, y_test)
