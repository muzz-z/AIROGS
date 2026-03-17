import os
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier

from preprocessing.utils import preprocess_image
from feature_extraction.utils import extract_features

DATASET_DIR = "dataset/train"

X, y = [], []
label_map = {"normal": 0, "glaucoma": 1}

for label in label_map:
    folder = os.path.join(DATASET_DIR, label)

    for file in os.listdir(folder):
        img_path = os.path.join(folder, file)

        img = preprocess_image(img_path)
        if img is None:
            continue

        features = extract_features(img)
        if features is None:
            continue

        X.append(features)
        y.append(label_map[label])

X = np.array(X)
y = np.array(y)

# Train-test split (IMPORTANT)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Balanced Random Forest
model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train, y_train)

# Evaluation
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))
print(classification_report(y_test, preds))

# Save model
joblib.dump(model, "glaucoma_model.pkl")
print("✅ Model saved")
