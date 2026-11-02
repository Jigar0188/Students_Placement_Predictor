
import os
import joblib
from model import train_model

# Create artifacts folder
os.makedirs("artifacts", exist_ok=True)

# Train the model
model, scaler, feature_columns, accuracy = train_model()

# Save everything required for prediction
artifacts = {
    "model": model,
    "scaler": scaler,
    "feature_columns": list(feature_columns),
}

joblib.dump(artifacts, "artifacts/placement_model.pkl")

print("\nModel training completed!")
print(f"Model accuracy: {accuracy:.2%}")
print("Model saved successfully!")
